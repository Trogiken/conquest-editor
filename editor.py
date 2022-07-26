from os import getenv, path, system
from xml.etree import ElementTree
from pathlib import Path


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

    def refresh(self):
        system('cls')
        print(self.splash)


class Save:
    def __init__(self):
        self.cmd = Terminal()
        self.appdata = str(Path(getenv("APPDATA")).parents[0])
        self.save = self.appdata + '\\LocalLow\\SteelRaven7\\RavenfieldSteam\\Saves\\autosave.xml'
        self.dom = None

        while not path.exists(self.save):
            self.save = input("Save not found | Enter path to Save; e.g: \\path\\to\\autosave.xml\n> ")
            self.cmd.refresh()
        self.dom = ElementTree.parse(self.save)

    def load(self):
        states = self.dom.findall('levels/LevelState')
        teams = self.dom.findall('resources/ConquestTeamResources')

        level_data = {}
        for c in states:
            name = c.find('objectName').text
            owner = c.find('owner').text
            battalions = c.find('battalions').text
            level = {name: {'owner': owner, 'battalions': battalions}}
            level_data.update(level)

        value = 1
        for n in self.dom.iter('int'):  # DEBUG
            if value == 1:
                print("\tEagle:")
                print("\t\tGain:")
                print(f'\t\t\tBattalions: {n.text}')
            elif value == 2:
                print(f'\t\t\tCoins: {n.text}')
            elif value == 3:
                print(f'\t\t\tResearch: {n.text}')
            elif value == 17:
                print("\t\tAvailable:")
                print(f'\t\t\tBattalions: {n.text}')
            elif value == 18:
                print(f'\t\t\tCoins: {n.text}')
            elif value == 19:
                print(f'\t\t\tResearch: {n.text}')
            elif value == 33:
                print("\tRaven:")
                print("\t\tGain:")
                print(f'\t\t\tBattalions: {n.text}')
            elif value == 34:
                print(f'\t\t\tCoins: {n.text}')
            elif value == 35:
                print(f'\t\t\tResearch: {n.text}')
            elif value == 49:
                print("\t\tAvailable:")
                print(f'\t\t\tBattalions: {n.text}')
            elif value == 50:
                print(f'\t\t\tCoins: {n.text}')
            elif value == 51:
                print(f'\t\t\tResearch: {n.text}')
            value += 1
        # resource_data = {}
        # for team in teams:
        #     print(team)
        #     for c in team:
        #         print(c)
        #         print(c.find('int').text)

        return level_data


def main():
    cmd = Terminal()
    cmd.refresh()
    save = Save()

    h = save.load()

    print("\n\tTiles:")
    for f in h:
        owner = h[f]['owner']
        if owner == '1':
            occ = 'Red'
        elif owner == '0':
            occ = 'Blue'
        else:
            occ = 'None'
        print(f"\t\t{f}:{occ}\n\t\t\tBattalions: {h[f]['battalions']}")


if __name__ == '__main__':
    main()
