import cv2
import numpy as np
import pickle
import json
from pathlib import Path

COR_SABRE = (255, 100, 0) 
ESPESSURA_CENTRO = 12
ESPESSURA_BRILHO = 50
INTENSIDADE_BRILHO_INTERNO = 2.0
INTENSIDADE_BRILHO_EXTERNO = 0.5
COMPRIMENTO_RASTRO = 10

def adicionar_sabre_realista(frame, p1, p2, cor_sabre, alpha=1.0):
    overlay = frame.copy()
    espessura_externa = max(1, int(ESPESSURA_BRILHO * alpha))
    cv2.line(overlay, p1, p2, cor_sabre, espessura_externa, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, INTENSIDADE_BRILHO_EXTERNO * alpha, frame, 1 - INTENSIDADE_BRILHO_EXTERNO * alpha, 0, frame)
    
    overlay = frame.copy()
    espessura_media = max(1, int(ESPESSURA_BRILHO * 0.6 * alpha))
    cv2.line(overlay, p1, p2, cor_sabre, espessura_media, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, 0.5 * alpha, frame, 1 - 0.5 * alpha, 0, frame)
    
    overlay = frame.copy()
    espessura_interna = max(1, int(ESPESSURA_BRILHO * 0.3 * alpha))
    cor_interna = tuple([min(255, int(c * 1.3)) for c in cor_sabre])
    cv2.line(overlay, p1, p2, cor_interna, espessura_interna, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, 0.7 * alpha, frame, 1 - 0.7 * alpha, 0, frame)
    
    overlay = frame.copy()
    espessura_centro = max(1, int(ESPESSURA_CENTRO * alpha))
    cv2.line(overlay, p1, p2, (255, 255, 255), espessura_centro, lineType=cv2.LINE_AA)
    cv2.addWeighted(overlay, INTENSIDADE_BRILHO_INTERNO * alpha, frame, 1 - INTENSIDADE_BRILHO_INTERNO * alpha, 0, frame)
    
    return frame

def marcar_cabo_manualmente(caminho_video, marcacoes_existentes=None):
    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        print(f" Erro ao abrir: {caminho_video}")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)

    print("=" * 70)
    print(" ETAPA 1: MARCAR O CABO DE VASSOURA")
    print("=" * 70)
    print(f" Total de frames: {total_frames}")
    print(f"  FPS: {fps}")
    print("\n INSTRUÇÕES:")
    print("1. Clique nas DUAS PONTAS do cabo (início e fim)")
    print("2. Pressione ESPAÇO para avançar pro próximo frame")
    print("3. Pressione 'S' para PULAR o frame atual")
    print("4. Pressione 'B' para VOLTAR 1 frame (não redesenha a marcação automaticamente)")
    print("5. Pressione 'D' para DELETAR a marcação do frame atual")
    print("6. Pressione 'Q' quando terminar de marcar (SALVA em JSON + pickle)")
    print("-" * 70)
    
    print("\n MODO DE MARCAÇÃO:")
    print("1. TODOS os frames (precisão máxima, mais demorado)")
    print("2. Frames espalhados (~20 frames, interpolação automática)")
    modo = input("\nEscolha o modo (1 ou 2): ").strip()

    frames_para_marcar = []
    if modo == "1":
        frames_para_marcar = list(range(0, total_frames))
        print(f"\n Modo selecionado: TODOS os {total_frames} frames")
        print("  Isso pode demorar! Use 'Q' pra parar quando quiser.")
    else:
        intervalo = max(1, total_frames // 20)
        for i in range(0, total_frames, intervalo):
            frames_para_marcar.append(i)
        print(f"\n Modo selecionado: ~{len(frames_para_marcar)} frames espalhados")

    print("-" * 70)

    marcacoes = [] if marcacoes_existentes is None else list(marcacoes_existentes)
    marcacoes_dict = {frame_num: (p1, p2) for frame_num, p1, p2 in marcacoes}

    pontos_temporarios = []
    frame_atual_idx = 0

    def encontrar_indice_marcacao(frame_num):
        for idx, (fnum, _, _) in enumerate(marcacoes):
            if fnum == frame_num:
                return idx
        return None

    def remover_marcacao(frame_num):
        idx = encontrar_indice_marcacao(frame_num)
        if idx is not None:
            marcacoes.pop(idx)
            marcacoes_dict.pop(frame_num, None)
            print(f" Marcacao do frame {frame_num} removida.")

    def salvar_marcacoes_arquivos(pickle_path='marcacoes_cabo.pkl', json_path='marcacoes_cabo.json'):
        try:
            with open(pickle_path, 'wb') as f:
                pickle.dump(marcacoes, f)
            json_list = []
            for frame_num, p1, p2 in marcacoes:
                json_list.append({
                    'frame': int(frame_num),
                    'p1': [int(p1[0]), int(p1[1])],
                    'p2': [int(p2[0]), int(p2[1])]
                })
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_list, f, indent=2)
            print(f"\n Marcações salvas em: {pickle_path} e {json_path}")
        except Exception as e:
            print(" Erro ao salvar marcações:", e)

    def mouse_callback(event, x, y, flags, param):
        nonlocal pontos_temporarios
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(pontos_temporarios) < 2:
                pontos_temporarios.append((x, y))
                print(f"   ✓ Ponto {len(pontos_temporarios)} marcado: ({x}, {y})")
                if len(pontos_temporarios) == 2:
                    print("   Cabo marcado neste frame! Pressione ESPAÇO para confirmar.")
            else:
                print("Já existem 2 pontos temporários neste frame. Pressione ESPAÇO para confirmar ou 'R' para resetar.")

    cv2.namedWindow('Marcar Cabo', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Marcar Cabo', mouse_callback)

    while frame_atual_idx < len(frames_para_marcar):
        frame_num = frames_para_marcar[frame_atual_idx]
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            frame_atual_idx += 1
            continue

        altura = frame.shape[0]
        escala = 1.0
        if altura > 720:
            escala = 720 / altura
            frame_display = cv2.resize(frame, None, fx=escala, fy=escala)
        else:
            frame_display = frame.copy()

        for i, ponto in enumerate(pontos_temporarios):
            cv2.circle(frame_display, ponto, 8, (0, 255, 0), -1)
            cv2.putText(frame_display, str(i+1), (ponto[0] + 15, ponto[1]),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if len(pontos_temporarios) == 2:
            cv2.line(frame_display, pontos_temporarios[0], pontos_temporarios[1], (0, 255, 255), 3)

        info_text = [
            f"Frame: {frame_num}/{total_frames}",
            f"Marcados: {len(marcacoes)} frames",
            f"Pontos temporarios: {len(pontos_temporarios)}/2",
            "",
            "Espaco = Proximo | S = Pular | B = Voltar | D = Deletar | Q = Finalizar (salvar)"
        ]

        y_offset = 30
        for texto in info_text:
            cv2.putText(frame_display, texto, (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
            y_offset += 30

        cv2.imshow('Marcar Cabo', frame_display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            if len(pontos_temporarios) == 2:
                if escala != 1.0:
                    p1 = (int(pontos_temporarios[0][0] / escala), int(pontos_temporarios[0][1] / escala))
                    p2 = (int(pontos_temporarios[1][0] / escala), int(pontos_temporarios[1][1] / escala))
                else:
                    p1, p2 = pontos_temporarios[0], pontos_temporarios[1]

                idx_exist = encontrar_indice_marcacao(frame_num)
                if idx_exist is not None:
                    marcacoes[idx_exist] = (frame_num, p1, p2)
                    print(f"Marcacao do frame {frame_num} atualizada.")
                else:
                    marcacoes.append((frame_num, p1, p2))
                    print(f"Frame {frame_num} salvo! Total: {len(marcacoes)} frames marcados")
                
                marcacoes_dict[frame_num] = (p1, p2)

                pontos_temporarios = []
                frame_atual_idx += 1
            else:
                print("Marque os 2 pontos antes de avançar!\n")

        elif key == ord('s'):
            print(f"  Frame {frame_num} pulado\n")
            pontos_temporarios = []
            frame_atual_idx += 1

        elif key == ord('b'):
            if frame_atual_idx > 0:
                frame_atual_idx -= 1
                pontos_temporarios = []
                print(f"⬅Voltando para frame {frames_para_marcar[frame_atual_idx]}")
            else:
                print("Já está no primeiro frame da sequência.")

        elif key == ord('d'):
            if frame_num in marcacoes_dict:
                remover_marcacao(frame_num)
            else:
                print("Nenhuma anotação neste frame para deletar.")
            pontos_temporarios = []

        elif key == ord('q'):
            if modo == "1":
                if len(marcacoes) >= 1:
                    salvar_marcacoes_arquivos()
                    break
                else:
                    print("Marque pelo menos 1 frame antes de finalizar.")
            else:
                if len(marcacoes) >= 5:
                    salvar_marcacoes_arquivos()
                    break
                else:
                    print(f"Marque pelo menos 5 frames! Você tem {len(marcacoes)}")

        elif key == ord('r'):
            pontos_temporarios = []
            print("Cliques temporários resetados para este frame.")


    cap.release()
    cv2.destroyAllWindows()
    return marcacoes

def processar_com_marcacoes(caminho_video_entrada, caminho_video_saida, marcacoes):
    cap = cv2.VideoCapture(caminho_video_entrada)
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 30)
    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("\n" + "=" * 70)
    print(" ETAPA 2: PROCESSANDO VÍDEO")
    print("=" * 70)
    print(f" Resolução: {largura}x{altura} @ {fps}fps")
    print(f"Total de frames: {total_frames}")
    print("-" * 70)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(caminho_video_saida, fourcc, fps, (largura, altura))

    marcacoes_dict = {frame_num: (p1, p2) for frame_num, p1, p2 in marcacoes}
    frames_marcados = sorted(marcacoes_dict.keys())

    posicoes_anteriores = []
    frame_atual = 0

    print("Processando...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_atual += 1
        porcentagem = (frame_atual / total_frames) * 100

        p1, p2 = None, None

        if frame_atual in marcacoes_dict:
            p1, p2 = marcacoes_dict[frame_atual]
        else:
            anterior = None
            posterior = None
            for fm in frames_marcados:
                if fm < frame_atual:
                    anterior = fm
                elif fm > frame_atual:
                    posterior = fm
                    break

            if anterior is not None and posterior is not None:
                p1_ant, p2_ant = marcacoes_dict[anterior]
                p1_post, p2_post = marcacoes_dict[posterior]
                t = (frame_atual - anterior) / (posterior - anterior)
                p1 = (int(p1_ant[0] + t * (p1_post[0] - p1_ant[0])),
                      int(p1_ant[1] + t * (p1_post[1] - p1_ant[1])))
                p2 = (int(p2_ant[0] + t * (p2_post[0] - p2_ant[0])),
                      int(p2_ant[1] + t * (p2_post[1] - p2_ant[1])))
            elif anterior is not None:
                p1, p2 = marcacoes_dict[anterior]
            elif posterior is not None:
                p1, p2 = marcacoes_dict[posterior]

        if p1 and p2:
            posicoes_anteriores.append((p1, p2))
            if len(posicoes_anteriores) > COMPRIMENTO_RASTRO:
                posicoes_anteriores.pop(0)

            for i, (pt1, pt2) in enumerate(posicoes_anteriores):
                alpha = ((i + 1) / len(posicoes_anteriores)) ** 1.5
                frame = adicionar_sabre_realista(frame, pt1, pt2, COR_SABRE, alpha)

        out.write(frame)
        print(f"Frame {frame_atual}/{total_frames} ({porcentagem:.1f}%)", end='\r')

    cap.release()
    out.release()

    print(f"\n\n{'=' * 70}")
    print(f" Vídeo processado: {caminho_video_saida}")
    print(f" Processo concluído!")
    print(f"{'=' * 70}")

def main():
    video_entrada = "video_original.mp4"
    video_saida = "video_com_sabre_final.mp4"
    pickle_path = 'marcacoes_cabo.pkl'
    json_path = 'marcacoes_cabo.json'

    print("\n" + " X " * 6)
    print("     PROCESSADOR DE SABRE DE LUZ - TREINAMENTO MANUAL")
    print("X " * 6 + "\n")
    
    marcacoes = None
    if Path(pickle_path).exists():
        try:
            with open(pickle_path, 'rb') as f:
                marcacoes = pickle.load(f)
            print(f" Encontrado arquivo de marcações: {pickle_path} ({len(marcacoes)} frames)")
            usar = input("Usar marcações existentes? (S/n): ").strip().lower()
            if usar == 'n':
                marcacoes = None
        except Exception as e:
            print("Falha ao carregar marcações (pickle):", e)
            marcacoes = None

    if not marcacoes:
        marcacoes = marcar_cabo_manualmente(video_entrada, marcacoes_existentes=None)
        if not marcacoes:
            print("Processo cancelado")
            return
    else:
        editar = input("Deseja editar as marcações existentes? (s/N): ").strip().lower()
        if editar == 's':
            marcacoes = marcar_cabo_manualmente(video_entrada, marcacoes_existentes=marcacoes)
            if not marcacoes:
                print(" Edição cancelada")
                return
            
    processar_com_marcacoes(video_entrada, video_saida, marcacoes)

if __name__ == "__main__":
    main()
