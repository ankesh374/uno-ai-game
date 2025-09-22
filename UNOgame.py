import tkinter as tk
from tkinter import messagebox
import random


class UnoGame:
    def __init__(self, root, num_players):
        self.root = root
        self.num_players = num_players
        self.players = [[] for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1
        self.deck = self.create_deck()
        self.discard_pile = []
        self.game_over = False

        self.colors = {"Red": "#FF4C4C", "Blue": "#2196F3", "Green": "#4CAF50", "Yellow": "#FFD700"}

        # GUI setup
        self.root.title("UNO Game")
        self.turn_label = tk.Label(root, text="Welcome to UNO!", font=("Arial", 14))
        self.turn_label.pack(pady=10)

        self.top_card_canvas = tk.Canvas(root, width=120, height=180, bg="white", highlightthickness=0)
        self.top_card_canvas.pack(pady=10)

        self.player_frame = tk.Frame(root)
        self.player_frame.pack(pady=20)

        self.log = tk.Text(root, height=10, width=60, bg="black", fg="white")
        self.log.pack(pady=10)

        self.deal_cards()
        self.start_game()

    def create_deck(self):
        colors = ["Red", "Blue", "Green", "Yellow"]
        values = [str(i) for i in range(10)] + ["Skip", "Reverse", "Draw Two"]
        deck = [(c, v) for c in colors for v in values for _ in range(2)]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        for player in self.players:
            for _ in range(7):
                player.append(self.deck.pop())
        self.discard_pile.append(self.deck.pop())

    def draw_card_canvas(self, canvas, card):
        canvas.delete("all")
        color, value = card
        bg = self.colors[color]
        canvas.create_rectangle(10, 10, 110, 170, fill=bg, outline="black", width=3)
        canvas.create_text(60, 90, text=value, font=("Arial", 18, "bold"), fill="white")

    def update_gui(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()

        # Update top card
        top_card = self.discard_pile[-1]
        self.draw_card_canvas(self.top_card_canvas, top_card)

        # Show current player’s hand if human
        if self.current_player == 0 and not self.game_over:
            for idx, card in enumerate(self.players[0]):
                c = tk.Canvas(self.player_frame, width=80, height=120, bg="white", highlightthickness=0)
                self.draw_card_on_hand(c, card)
                c.grid(row=0, column=idx, padx=5)
                c.bind("<Button-1>", lambda e, i=idx: self.play_card(0, i))

            draw_btn = tk.Button(self.player_frame, text="Draw", command=lambda: self.draw_card(0))
            draw_btn.grid(row=1, columnspan=len(self.players[0]), pady=10)

    def draw_card_on_hand(self, canvas, card):
        color, value = card
        bg = self.colors[color]
        canvas.create_rectangle(5, 5, 75, 115, fill=bg, outline="black", width=2)
        canvas.create_text(40, 60, text=value, font=("Arial", 12, "bold"), fill="white")

    def play_card(self, player_idx, card_idx):
        if self.game_over:
            return

        player = self.players[player_idx]
        card = player[card_idx]
        top_card = self.discard_pile[-1]

        if card[0] == top_card[0] or card[1] == top_card[1]:
            self.discard_pile.append(card)
            del player[card_idx]
            self.log.insert(tk.END, f"Player {player_idx} played {card[0]} {card[1]}\n")

            if card[1] == "Reverse":
                self.direction *= -1
            elif card[1] == "Skip":
                self.current_player = (self.current_player + self.direction) % self.num_players
            elif card[1] == "Draw Two":
                next_player = (self.current_player + self.direction) % self.num_players
                self.players[next_player].extend([self.deck.pop(), self.deck.pop()])
                self.log.insert(tk.END, f"Player {next_player} draws 2 cards!\n")

            if not player:
                self.end_game(player_idx)
                return
        else:
            self.log.insert(tk.END, f"Invalid move! {card[0]} {card[1]} cannot be played.\n")

        self.next_turn()

    def draw_card(self, player_idx):
        if self.deck:
            card = self.deck.pop()
            self.players[player_idx].append(card)
            self.log.insert(tk.END, f"Player {player_idx} draws a card\n")
        self.next_turn()

    def next_turn(self):
        if self.game_over:
            return

        self.current_player = (self.current_player + self.direction) % self.num_players
        self.turn_label.config(text=f"Player {self.current_player}'s turn")

        if self.current_player == 0:
            self.update_gui()
        else:
            self.root.after(1000, self.ai_play)

    def ai_play(self):
        if self.game_over:
            return

        player = self.players[self.current_player]
        top_card = self.discard_pile[-1]

        for idx, card in enumerate(player):
            if card[0] == top_card[0] or card[1] == top_card[1]:
                self.play_card(self.current_player, idx)
                return

        self.draw_card(self.current_player)

    def start_game(self):
        self.update_gui()
        self.turn_label.config(text="Your turn!")

    def end_game(self, player_idx):
        self.game_over = True
        if player_idx == 0:
            messagebox.showinfo("UNO", "🎉 You win!")
        else:
            messagebox.showinfo("UNO", f"🤖 AI {player_idx} wins!")
        self.root.after(1000, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    while True:
        try:
            n = int(input("Enter number of players (2-4): "))
            if 2 <= n <= 4:
                break
        except Exception:
            pass
    game = UnoGame(root, n)
    root.mainloop()
