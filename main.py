import subprocess
import sys
import os
import tkinter as tk

# main.py - SO MENU, NAO MEXER NOS JOGOS
# Chama cada jogo original separado, sem mudar nada dentro deles
# Cobrinha = cobrinha.py (pygame)
# Tetris = tetris.py (pygame)
# Bomberman = bomberman.py (tkinter + nes.mp3)

PIX = "51993359782"

def rodar(arquivo):
    # Roda o jogo original em processo separado, sem tocar no codigo dele
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, arquivo)
    subprocess.Popen([sys.executable, caminho])

root = tk.Tk()
root.title("CORANGE - 3 JOGOS - PIX 51993359782")
root.geometry("400x420")
root.resizable(False, False)
root.configure(bg="black")

tk.Label(root, text="CORANGE SISTEMAS", font=("Arial", 22, "bold"), bg="black", fg="#ffcc00").pack(pady=15)
tk.Label(root, text="3 JOGOS", font=("Arial", 16, "bold"), bg="black", fg="white").pack()
tk.Label(root, text="PIX 51993359782", font=("Arial", 14, "bold"), bg="black", fg="#00ff88").pack(pady=10)

tk.Button(root, text="🐍  COBRINHA", font=("Arial", 16, "bold"), bg="#00ff88", fg="black", width=22, pady=10,
          command=lambda: rodar("cobrinha.py")).pack(pady=8)

tk.Button(root, text="🧱  TETRIS", font=("Arial", 16, "bold"), bg="#00ccff", fg="black", width=22, pady=10,
          command=lambda: rodar("tetris.py")).pack(pady=8)

tk.Button(root, text="💣  BOMBERMAN", font=("Arial", 16, "bold"), bg="#ffcc00", fg="black", width=22, pady=10,
          command=lambda: rodar("bomberman.py")).pack(pady=8)

tk.Label(root, text="Som: nes.mp3 no Bomberman\nBeep no Cobrinha e Tetris\nNada foi alterado nos jogos", 
         font=("Arial", 10), bg="black", fg="gray").pack(pady=15)

root.mainloop()
