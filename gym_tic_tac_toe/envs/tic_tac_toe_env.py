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
        # pack action in a tuple
        move = int(action / self.board.size), action % self.board.size, 1 if self.current_player == 0 else -1
        # check for move legality; if not - end the game and return -1 as the reward
        if self.board.board[move[0], move[1]] != 0:
            return self.board.board, -1, True, self.info
        # introduce the move and check for game end
        game_won, game_ended = self.board.add_move(move)
        # change current player
        self.current_player = abs(self.current_player - 1)
        return self.board.board, 1 if game_won else 0, game_ended, self.info


