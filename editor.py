from os import getenv, path, system
from xml.etree import ElementTree
from pathlib import Path
import platform


class Terminal:
    """
    Terminal formatting

        to print xml data with refresh() you must assign data to Terminal().data

    Attributes
    ----------
    data : list
        save data
    """
    def __init__(self):
        """Constructs all necessary attributes for the Save object"""
        self.data = None

    @staticmethod
    def delimit(s, delimiter, n, t):
        """
        Add '\n' every (n) (delimiter) to given string (s)

        Parameters
        ----------
        s : str
            string to delimit
        delimiter : str
            character(s) that will be iterated
        n : int
            how many iterations of the delimiter (delimiter) until '\n' is added to the given string (s)
        t : int
            indent amount
        """
        segments = s.split(delimiter)  # splits string by delimiter
        for i, seg in enumerate(segments):
            if i % n == 0 and i != 0:
                segments[i] = '\n' + ('\t' * t) + seg  # prepend '\n' to segment
        return delimiter.join(segments)  # join segments

    @staticmethod
    def clear():
        os = platform.system()
        if os == 'Windows':
            system('cls')
        else:
            system('clear')

    @staticmethod
    def print(s, t=1, space_above=None, space_below=None):
        """
        Format and print string

        Parameters
        ----------
        s : str
            printed string
        t : int
            indent amount
        space_above : int
            number of blank lines above string (starts at 0)
        space_below : int
            number of blank line below string (starts at 0)
        """
        if space_above is not None:
            print('\n' * space_above)
        print(('\t' * t) + s)
        if space_below is not None:
            print('\n' * space_below)

    @staticmethod
    def q_print(s, t=1, space_above=None, space_below=None):
        """
        Format question and return input

        Parameters
        ----------
        s : str
            printed string
        t : int
            indent amount
        space_above : int
            number of blank lines above string (starts at 0)
        space_below : int
            number of blank line below string (starts at 0)
        """
        if space_above is not None:
            print('\n' * space_above)
        indent = '\t' * t
        if s:
            resp = input(indent + f"{s}\n" + indent + "> ")
        else:
            resp = input(indent + "> ")
        if space_below is not None:
            print('\n' * space_below)
        return resp

    def refresh(self, show_less=False):
        """
        Display splash and xml data at the top of terminal

        Parameters
        ----------
        show_less : bool
            xml data will NOT be displayed even if (self.data) is assigned
        """
        self.clear()
        print(r"""
          _____                _ _              _       _____    _ _ _             
         |_   _| __ ___   __ _(_) | _____ _ __ ( )___  | ____|__| (_) |_ ___  _ __ 
           | || '__/ _ \ / _` | | |/ / _ \ '_ \|// __| |  _| / _` | | __/ _ \| '__|
           | || | | (_) | (_| | |   <  __/ | | | \__ \ | |__| (_| | | || (_) | |   
           |_||_|  \___/ \__, |_|_|\_\___|_| |_| |___/ |_____\__,_|_|\__\___/|_|   
                         |___/                                                     
        ----------------------------------------------------------------------------
        """)

        if self.data is not None and show_less is False:
            h = self.data

            for p_id, p_info in h[1].items():
                if p_id == 0:
                    team = 'Eagle'
                else:
                    team = 'Raven'

                tech_items = self.delimit(', '.join(h[2][p_id]), ',', 6, 3)

                print(f"\t{team}:\n"
                      f"\t\tGain:\n\t\t\tCoins: {p_info['g_coins']}\n\t\t\tResearch: {p_info['g_research']}\n"
                      f"\t\tAvailable:\n\t\t\tCoins: {p_info['c_coins']}\n\t\t\tResearch: {p_info['c_research']}\n"
                      f"\t\tTech: {tech_items}")

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
        print('#' * 92)


class Save:
    """Manage xml file"""
    def __init__(self):
        """Constructs all necessary attributes for the Save object"""
        self.cmd = Terminal()
        # Feature: List of possible cross-platform paths to autosave, (for i in paths: if path exists: self.save = i)
        try:
            self.appdata = str(Path(getenv("APPDATA")).parents[0])
        except TypeError:
            self.appdata = 'ENV_Not_Found'
        self.save = self.appdata + '\\LocalLow\\SteelRaven7\\RavenfieldSteam\\Saves\\autosave.xml'
        self.dom = None

        while not path.exists(self.save):  # Feature: Save location if not found
            self.cmd.refresh()
            self.save = self.cmd.q_print("Save not found | Enter path to Save; e.g: \\path\\to\\autosave.xml")
        self.dom = ElementTree.parse(self.save)

    def load(self):
        """Parse xml file, returns list of dictionarys for Tile (0), Team (1), and Tech (2) data"""
        tile_data = {}
        for c in self.dom.findall('levels/LevelState'):
            name = c.find('objectName').text
            owner = c.find('owner').text
            battalions = c.find('battalions').text
            level = {name: {'owner': owner, 'battalions': battalions}}
            tile_data.update(level)

        tech_data = {}
        iteration = 0
        for ids in self.dom.findall('teamTechStatus/TechStatus/unlockedTechIds'):
            if iteration == 0:
                tech_data[iteration] = []
            elif iteration == 1:
                tech_data[iteration] = []
            else:
                raise 'Unknown TechId Tag'
            for e in ids:
                tech_data[iteration].append(e.text)
            iteration += 1

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

        return [tile_data, team_data, tech_data]

    def update(self, category_id, variable, value):
        """
        Update data in xml file

        Parameters
        ----------
        category_id : int
            index from save.load()
        variable : str
            element/tag to be updated
        value : str
            new value of element/tag
        """
        if category_id == 0:
            pass
        elif category_id == 1:
            if variable in ['eg_coins', 'eg_research', 'ec_coins', 'ec_research', 'rg_coins', 'rg_research', 'rc_coins', 'rc_research']:
                iteration = 1
                for n in self.dom.iter('int'):
                    print(iteration)
                    if iteration == 1 and variable == 'eg_coins':
                        n.text = str(int(value))
                    elif iteration == 2 and variable == 'eg_research':
                        n.text = str(int(value))
                    elif iteration == 17 and variable == 'ec_coins':
                        n.text = str(int(value))
                    elif iteration == 18 and variable == 'ec_research':
                        n.text = str(int(value))
                    elif iteration == 33 and variable == 'rg_coins':
                        n.text = str(int(value))
                    elif iteration == 34 and variable == 'rg_research':
                        n.text = str(int(value))
                    elif iteration == 49 and variable == 'rc_coins':
                        n.text = str(int(value))
                    elif iteration == 50 and variable == 'rc_research':
                        n.text = str(int(value))
                    iteration += 1
                self.dom.write(self.save)
            else:
                raise 'Invalid Variable'
        elif category_id == 2:
            pass
        else:
            raise 'Invalid Category ID'


def main(s, c):
    """Program Loop"""
    save = s
    cmd = c
    cmd.data = save.load()

    main_header = 'MAIN'

    while True:
        cmd.refresh()
        cmd.print(f"[{main_header}]", t=2)
        cmd.print("Eagle : 1")
        cmd.print("Raven : 2")
        cmd.print("Exit  : 0")

        try:
            resp = int(cmd.q_print('', space_above=0))
        except ValueError:
            continue

        if resp in [1, 2, 0]:
            if resp == 1:
                team_header = 'EAGLE'
                team = 'e'
            elif resp == 2:
                team_header = 'RAVEN'
                team = 'r'
            else:
                return True
        else:
            continue

        while True:
            cmd.refresh()
            cmd.print(f"[{team_header}]", t=2)
            cmd.print("Set  : 1")
            cmd.print("Back : 0")

            try:
                resp = int(cmd.q_print('', space_above=0))
            except ValueError:
                continue

            if resp in [1, 0]:
                if resp == 1:
                    action_header = 'SET'
                else:
                    break
            else:
                continue

            while True:
                cmd.refresh()
                cmd.print(f"[{action_header}]", t=2)
                cmd.print("Coins    : 1")
                cmd.print("Research : 2")
                # Feature: (3) Tech
                cmd.print("Back     : 0")

                try:
                    opt = int(cmd.q_print('', space_above=0))
                except ValueError:
                    continue

                if opt in [1, 2, 0]:
                    if opt == 1:
                        while True:
                            cmd.refresh(show_less=True)
                            try:
                                num = int(cmd.q_print('Amount of Coins', space_above=0))
                                save.update(1, f'{team}c_coins', num)
                                cmd.data = save.load()
                                break
                            except ValueError:
                                continue
                    elif opt == 2:
                        while True:
                            cmd.refresh(show_less=True)
                            try:
                                num = int(cmd.q_print('Amount of Research', space_above=0))
                                save.update(1, f'{team}c_research', num)
                                cmd.data = save.load()
                                break
                            except ValueError:
                                continue
                    else:
                        break
                else:
                    continue


if __name__ == '__main__':
    Save = Save()
    Terminal = Terminal()
    z = main(s=Save, c=Terminal)
    if z:  # if program exited naturally
        Terminal.clear()
        print("Goodbye...")
