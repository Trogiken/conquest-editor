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
    show_eagle : bool
        display eagle team data
    show_raven : bool
        display raven team data
    """

    def __init__(self):
        """Constructs all necessary attributes for the Save object"""
        self.data = None

        self.show_eagle = True
        self.show_raven = True

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

    def refresh(self, show_less=False, tile_data=True, team_data=True, tech_data=True):
        """
        Display splash and xml data at the top of terminal
            change class attribute (eagle/raven) to True or False to display/hide specific team

        Parameters
        ----------
        show_less : bool
            xml data will NOT be displayed even if (self.data) is assigned
        tile_data : bool
            display tile data
        team_data : bool
            display team data
        tech_data : bool
            display tech data
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
                    team_name = 'Eagle'
                    if self.show_eagle is False:
                        continue
                else:
                    team_name = 'Raven'
                    if self.show_raven is False:
                        continue

                if team_data or tech_data:
                    print(f"\t{team_name}:")
                    if team_data:
                        print(f"\t\tGain:\n\t\t\tCoins: {p_info['g_coins']}\n\t\t\tResearch: {p_info['g_research']}\n"
                              f"\t\tAvailable:\n\t\t\tCoins: {p_info['c_coins']}\n\t\t\tResearch: {p_info['c_research']}")
                    if tech_data:
                        tech_items = self.delimit(', '.join(h[2][p_id]), ',', 6, 3)
                        print(f"\t\tTech: {tech_items}")

            if tile_data:
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

    def tile_update(self, tag, tile, value):
        if tag in ['owner', 'battalions']:
            for c in self.dom.findall('levels/LevelState'):
                name = c.find('objectName').text
                if name == tile:
                    c.find(tag).text = str(int(value))
                    self.dom.write(self.save)
                else:
                    continue
        else:
            raise 'Invalid Tag'

    def resource_update(self, variable, value):
        if variable in ['eg_coins', 'eg_research', 'ec_coins', 'ec_research', 'rg_coins', 'rg_research', 'rc_coins', 'rc_research']:
            iteration = 1
            for n in self.dom.iter('int'):
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

    def tech_update(self):
        pass


class Editor:
    """
    Program class

    Attributes
    ----------
    save : object
        Save()
    cmd : object
        Terminal()
    """
    def __init__(self, save, terminal):
        """Constructs all necessary attributes for the Editor object"""
        self.save = save
        self.cmd = terminal

        self.main_header = 'MAIN'
        self.team_header = ''
        self.category_header = ''

    def _team_menu(self):
        """team management"""
        while True:
            self.cmd.refresh()
            self.cmd.print(f"[{self.main_header}/{self.team_header}]", t=2)
            self.cmd.print("Resource  : 1")
            self.cmd.print("Tech      : 2")
            self.cmd.print("Back      : 0")

            try:
                resp = int(self.cmd.q_print('', space_above=0))
            except ValueError:
                continue

            if resp in [1, 2, 0]:
                if resp == 1:
                    self.category_header = 'RESOURCE'
                    while True:
                        self.cmd.refresh(tile_data=False, tech_data=False)
                        self.cmd.print(f"[{self.main_header}/{self.team_header}/{self.category_header}]", t=2)
                        self.cmd.print("Coins    : 1")
                        self.cmd.print("Research : 2")
                        self.cmd.print("Back     : 0")

                        try:
                            opt = int(self.cmd.q_print('', space_above=0))
                        except ValueError:
                            continue

                        if opt in [1, 2, 0]:
                            if opt == 1:
                                t = 'COINS'
                                s = 'Amount of Coins'
                                v = f'{self.team_header[0].lower()}c_coins'
                            elif opt == 2:
                                t = 'RESEARCH'
                                s = 'Amount of Research'
                                v = f'{self.team_header[0].lower()}c_research'
                            else:
                                break
                        else:
                            continue

                        while True:
                            self.cmd.refresh(tile_data=False, tech_data=False)
                            self.cmd.print(f"[{self.main_header}/{self.team_header}/{self.category_header}/{t}]", t=2)
                            try:
                                num = int(self.cmd.q_print(s + ' | Back: 0', space_above=0))
                            except ValueError:
                                continue
                            if num != 0:
                                self.save.resource_update(v, num)
                                self.cmd.data = self.save.load()
                                break
                            else:
                                break
                elif resp == 2:
                    self.category_header = 'TECH'
                    while True:
                        self.cmd.refresh(team_data=False, tile_data=False)
                        self.cmd.print(f"[{self.main_header}/{self.team_header}/{self.category_header}]", t=2)
                        self.cmd.print("Add        : 1")
                        self.cmd.print("Del        : 2")
                        self.cmd.print("Add All    : 3")
                        self.cmd.print("Remove All : 4")
                        self.cmd.print("Back       : 0")

                        try:
                            opt = int(self.cmd.q_print('', space_above=0))
                        except ValueError:
                            continue

                        if opt in [1, 2, 0]:
                            if opt == 1:
                                pass
                            elif opt == 2:
                                pass
                            elif opt == 3:
                                pass
                            elif opt == 4:
                                pass
                            else:
                                break
                else:  # End of menu
                    break
            else:
                continue

    def _tile_menu(self):
        """tile management"""
        while True:
            self.cmd.refresh(team_data=False, tech_data=False)
            self.cmd.print(f"[{self.main_header}/{self.category_header}]", t=2)
            self.cmd.print("Owner        : 1")
            self.cmd.print("Battalions   : 2")
            self.cmd.print("Back         : 0")

            try:
                opt = int(self.cmd.q_print('', space_above=0))
            except ValueError:
                continue

            if opt in [1, 2, 0]:
                if opt == 1:
                    t = 'OWNER'
                    s = 'Eagle=1, Raven=2, None=-1'
                elif opt == 2:
                    t = 'BATTALIONS'
                    s = 'Number of battalions (Max is 3)'
                else:  # End of menu
                    break

                tile_names = []
                for c in self.save.dom.findall('levels/LevelState'):
                    name = c.find('objectName').text
                    tile_names.append(name)
                while True:
                    self.cmd.refresh(team_data=False, tech_data=False)
                    self.cmd.print(f"[{self.main_header}/{self.category_header}/{t}]", t=2)
                    tile_name = self.cmd.q_print('Name of tile you want to edit | Back : 0', space_above=0)
                    if tile_name != '0':
                        if tile_name not in tile_names:
                            continue
                    else:
                        break
                    while True:
                        self.cmd.refresh(team_data=False, tech_data=False)
                        self.cmd.print(f"[{self.main_header}/{self.category_header}/{t}]", t=2)
                        try:
                            value = int(self.cmd.q_print(s + ' | Back: 0', space_above=0))
                        except ValueError:
                            continue

                        tag = t.lower()
                        if value != 0:
                            if tag == 'owner':
                                if value in [1, 2, -1]:
                                    if value == 1:  # 0 reps eagle
                                        value = 0
                                    elif value == 2:  # 1 reps raven
                                        value = 1
                                else:
                                    continue
                            elif tag == 'battalions':
                                if not 3 >= value >= 0:  # Max 3, Min 0
                                    continue
                            self.save.tile_update(tag, tile_name, value)
                            self.cmd.data = self.save.load()
                            break
                        else:
                            break
            else:
                continue

    def run(self):
        """Program Loop"""
        while True:
            self.cmd.data = self.save.load()
            self.cmd.show_raven = True
            self.cmd.show_eagle = True
            self.cmd.refresh()
            self.cmd.print(f"[{self.main_header}]", t=2)
            self.cmd.print("Eagle : 1")
            self.cmd.print("Raven : 2")
            self.cmd.print("Tile  : 3")
            self.cmd.print("Exit  : 0")

            try:
                resp = int(self.cmd.q_print('', space_above=0))
            except ValueError:
                continue

            if resp in [1, 2, 3, 0]:
                if resp == 1:
                    self.team_header = 'EAGLE'
                    self.cmd.show_raven = False
                    self._team_menu()
                elif resp == 2:
                    self.team_header = 'RAVEN'
                    self.cmd.show_eagle = False
                    self._team_menu()
                elif resp == 3:
                    self.category_header = 'TILE'
                    self._tile_menu()
                else:  # Exit
                    return True
            else:
                continue


if __name__ == '__main__':
    editor = Editor(save=Save(), terminal=Terminal())
    z = editor.run()
    if z:  # if program exited naturally
        Terminal.clear()
        print("Goodbye...")
