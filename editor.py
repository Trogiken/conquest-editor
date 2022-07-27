from os import getenv, path, system
from xml.etree import ElementTree
from pathlib import Path
# n.text = str(int(10))  # if you can identify them use n.text to change the value of the specific <int\>
# self.dom.write(self.save)

class Terminal:
    def __init__(self):
        self.splash = r"""
          _____                _ _              _       _____    _ _ _             
         |_   _| __ ___   __ _(_) | _____ _ __ ( )___  | ____|__| (_) |_ ___  _ __ 
           | || '__/ _ \ / _` | | |/ / _ \ '_ \|// __| |  _| / _` | | __/ _ \| '__|
           | || | | (_) | (_| | |   <  __/ | | | \__ \ | |__| (_| | | || (_) | |   
           |_||_|  \___/ \__, |_|_|\_\___|_| |_| |___/ |_____\__,_|_|\__\___/|_|   
                         |___/                                                     
        ----------------------------------------------------------------------------
        """

    def refresh(self, add=''):
        system('cls')
        print(self.splash)
        save = Save()

        h = save.load()

        for p_id, p_info in h[1].items():
            if p_id == 0:
                team = 'Eagle'
            else:
                team = 'Raven'

            print(f"\t{team}:\n"
                  f"\t\tGain:\n\t\t\tCoins:{p_info['g_coins']}\n\t\t\tResearch:{p_info['g_research']}\n"
                  f"\t\tAvailable:\n\t\t\tCoins:{p_info['c_coins']}\n\t\t\tResearch:{p_info['c_research']}")

        print("\n\tTiles:")
        for f in h[0]:
            owner = h[0][f]['owner']
            if owner == '0':
                occ = 'Eagle'
            elif owner == '1':
                occ = 'Raven'
            else:
                occ = 'None'
            print(f"\t\t{f}:{occ}\n\t\t\tBattalions: {h[0][f]['battalions']}")


class Save:
    def __init__(self):
        self.cmd = Terminal()
        self.appdata = str(Path(getenv("APPDATA")).parents[0])
        self.save = self.appdata + '\\LocalLow\\SteelRaven7\\RavenfieldSteam\\Saves\\autosave.xml'
        self.dom = None

        while not path.exists(self.save):
            self.save = input("\tSave not found | Enter path to Save; e.g: \\path\\to\\autosave.xml\n> ")
            self.cmd.refresh()
        self.dom = ElementTree.parse(self.save)

    def load(self):
        level_data = {}
        for c in self.dom.findall('levels/LevelState'):
            name = c.find('objectName').text
            owner = c.find('owner').text
            battalions = c.find('battalions').text
            level = {name: {'owner': owner, 'battalions': battalions}}
            level_data.update(level)

        team_data = {}

        eg_coins = '?'
        eg_research = '?'
        ec_coins = '?'
        ec_research = '?'
        rg_coins = '?'
        rg_research = '?'
        rc_coins = '?'
        rc_research = '?'
        value = 1
        for n in self.dom.iter('int'):
            if value == 1:
                eg_coins = n.text
            elif value == 2:
                eg_research = n.text
            elif value == 17:
                ec_coins = n.text
            elif value == 18:
                ec_research = n.text
            elif value == 33:
                rg_coins = n.text
            elif value == 34:
                rg_research = n.text
            elif value == 49:
                rc_coins = n.text
            elif value == 50:
                rc_research = n.text
            value += 1

        team_data[0] = {}
        team_data[1] = {}

        team_data[0]['g_coins'] = eg_coins
        team_data[0]['g_research'] = eg_research
        team_data[0]['c_coins'] = ec_coins
        team_data[0]['c_research'] = ec_research
        team_data[1]['g_coins'] = rg_coins
        team_data[1]['g_research'] = rg_research
        team_data[1]['c_coins'] = rc_coins
        team_data[1]['c_research'] = rc_research

        return [level_data, team_data]


def main():
    cmd = Terminal()
    cmd.refresh()


if __name__ == '__main__':
    main()
