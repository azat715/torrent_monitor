import fire
from torrent.show import show

def cli():
    fire.Fire(fire.Fire({
      'show': show,
  }))
