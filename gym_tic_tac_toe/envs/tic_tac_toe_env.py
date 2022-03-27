import gym
from gym import spaces
from gym_tic_tac_toe.envs.board import Board


class TTTEnv(gym.Env):
    metadata = {'render_modes': ['ansi']}

    @property
    def info(self):
        return {
            'player': self.current_player,
            'action_mask': self.board.get_legal_moves()
        }

    def __init__(self, board_size):
        super(TTTEnv, self).__init__()
        # define action and observation spaces
        self.action_space = spaces.Discrete(board_size * board_size)
        self.observation_space = spaces.Box(high=1, low=-1, shape=(board_size, board_size), dtype=int)
        # initialize state
        self.board = Board(board_size)
        self.current_player = 0
        self.winning_player = -1

    def reset(self, *, seed=None, return_info=False, options=None):
        # reset state
        self.board.reset()
        self.current_player = 0
        return self.board.board if not return_info else (self.board.board, self.info)

    def render(self, mode="ansi"):
        # currently only supporting ansi render
        if mode == 'ansi':
            print(self.board)

    def step(self, action):
        reward = 0
        # pack action in a tuple
        move = int(action / self.board.size), action % self.board.size, 1 if self.current_player == 0 else -1
        # check for move legality; if not - end the game and return -1 as the reward
        # if the game has already ended - ignore move
        if self.board.board[move[0], move[1]] != 0 and not self.board.game_ended:
            return self.board.board, -10, True, self.info
        # introduce the move and check for game end
        game_won, game_ended = self.board.add_move(move)
        # register winning player
        if game_ended and self.winning_player == -1:
            self.winning_player = self.current_player if game_won else -2
        # determine the reward: 1 for player who won, -1 for player who lost, 0.5 to both in the event of the draw
        if game_ended:
            if self.winning_player == -2:
                reward = 0.5
            elif self.winning_player == self.current_player:
                reward = 1
            else:
                reward = -1

        # change current player
        self.current_player = abs(self.current_player - 1)
        return self.board.board, reward, game_ended, self.info


