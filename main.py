    def set_direcao(self, dl, dc):
        # Guarda a direção que tu quer - igual Atari
        self._dir_desejada = (dl, dc)
        # Se for virar 180 graus (voltar), vira na hora
        if self._dir_atual == (-dl, -dc):
            self._dir_atual = (dl, dc)
            self._dir_desejada = (dl, dc)
            return
        # Se ainda não tem movimento automático, liga
        if not self._event_andar:
            self._event_andar = Clock.schedule_interval(lambda dt: self.tentar_mover(), 0.14)

    def tentar_mover(self):
        if self.game_over: 
            return
        # 1 - Primeiro tenta ir pra onde tu CLICOU
        if self._dir_desejada != (0,0):
            nl = self.player[0] + self._dir_desejada[0]
            nc = self.player[1] + self._dir_desejada[1]
            if self.pode_andar(nl, nc, fantasma=False):
                self._dir_atual = self._dir_desejada
                self.mover(self._dir_atual[0], self._dir_atual[1])
                return
        # 2 - Se não deu pra virar, continua indo reto
        if self._dir_atual != (0,0):
            nl = self.player[0] + self._dir_atual[0]
            nc = self.player[1] + self._dir_atual[1]
            if self.pode_andar(nl, nc, fantasma=False):
                self.mover(self._dir_atual[0], self._dir_atual[1])
                return
