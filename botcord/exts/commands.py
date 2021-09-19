import os

from discord.ext.commands import Cog as Cog_

from botcord.configs import YAML


# noinspection PyAttributeOutsideInit
class Cog(Cog_):
    def config_init(self, __file__, path='configs.yml'):
        """PASS THE __file__ VARIABLE IN AS AN ARGUMENT FROM THE EXTENSION FILE,
        SO THE CONFIG PATH IS IN THE EXTENSION'S FOLDER AND NOT IN THE BOTCORD FILES HERE"""
        self._config_dir = f'{os.path.dirname(os.path.abspath(__file__))}/{path}'
        self._config = None
        self._configed = True

    def save_config(self):
        with open(self._config_dir, mode='w', encoding='UTF-8') as file:
            YAML.dump(self.config, file)

    def update_config(self):
        self._config = self._load_config()

    def _load_config(self):
        with open(self._config_dir, mode='a+', encoding='UTF-8') as wfile:
            wfile.seek(0)
            wloaded = YAML.load(wfile)
            if not wloaded:
                wloaded = {}
            return wloaded

    @property
    def config(self) -> dict:
        if not getattr(self, '_configed', False):
            raise AttributeError(f'type {type(self)} {self.__name__} has no attribute \'config\' \n'
                                 f'NOTE: Please call \'config_init()\' if you wish to utilize config files for this Cog.')

        if self._config is None:
            self._config = self._load_config()
        return self._config

    def cog_unload(self):
        self.save_config()
