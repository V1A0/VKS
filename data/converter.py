from PIL import Image, ImageDraw, ImageFont
import sqlite3
import datetime
import json
from os import walk, makedirs


class statistic:
    oap = 0  # OAP - Online Activity Percentage
    maxsd = 0  # MSD - Maximum Session Duration
    minsd = 9223372036854775806  # MIN session duration
    date = ''


class person(statistic):
    user_id = ''
    pic = ''
    profpic = 'data/pic/'
    about = {}

    def mk_statistic(self, date, path, alt):
        return f"""
            <details>
                <summary>{date}</summary>
                <img class = "stat" src = "data/pic/{path}" alt = "{alt}" width=75%>
                <div class="dayinfo">
                Online activity percentage: {self.oap} %
                </div>
                
                <div class="dayinfo">
                Maximum session duration: {self.maxsd} minutes
                </div>
                                
                <div class="dayinfo">
                Minimum session duration: {self.minsd} minutes
                </div>
            </details>
"""

    def mk_hat(self, content):
        return_ = f"""
            <div class="userinfo">
                <div class="username">{content.get('Name')}</div>
"""

        for title in content:
            if title != 'Name':
                return_ += f"""
                <div class="Menu__itemTitle">
                    {title}:   <a class="Menu__itemCount">{content[title]}</a>
                </div>"""



        return_ += f"""
            </div>
        
            <div class="profpic">
                <img src = "data/pic/{self.pic}" alt = "{self.pic}" class="profpic">
            </div>
        """

        return return_


def mkspic():
    class data:
        h = 0
        m = 0
        stat = 0

        def __init__(self, args):
            self.h, self.m, self.stat = args[0], args[1], args[2]

    print("\nVisualising data to graphics...\n")

    dir = []
    for (dirpath, dirnames, filenames) in walk('data/db'):
        dir.extend(filenames)
        break

    for dbfile in dir:
        try:
            conn = sqlite3.connect('data/db/' + dbfile)
            db = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for tab in db:
                print(tab[0], ' DONE')
                if tab[0][0] == 'T':
                    items = []
                    try:
                        cursor = conn.execute('SELECT HOURS, MINUTES, STATE FROM ' + tab[0])
                    except sqlite3.OperationalError:
                        cursor = ''

                    for item in cursor:
                        items.append(data(item))

                    makedirs('data/pic', exist_ok=True)
                    pic = Image.open('data/pic/defaultpic.png')
                    draw = ImageDraw.Draw(pic)

                    font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 90)
                    date_obj = datetime.datetime.strptime(tab[0], "T%d_%m_%Y")
                    text = date_obj.strftime("%d %b %Y")
                    draw.text((540, 10), text, (0, 0, 0), font=font)
                    draw.text((535, 5), text, (255, 255, 255), font=font)

                    sx = 4
                    sy = 0
                    for i in range(len(items)):
                        x, y = (73, 401) if items[i].h < 6 else (73, 699) if items[i].h < 12 \
                            else (73, 1053) if items[i].h < 18 else (73, 1351)

                        x += (items[i].h % 6) * 60 * 4 + (items[i].m * 4)

                        if items[i].stat == 1:
                            sy = 8 if items[i - 1].stat == 2 else sy + 1 if sy == 176 else sy + 8 if sy < 176 else sy

                            draw.rectangle((x + 1, y, x + sx, y - sy), fill=(0 + sy, 255 - (sy // 5), 0))

                        elif items[i].stat == 0:
                            sy = 8
                            draw.rectangle((x + 1, y, x + sx, y - 2), fill=(0, 0, 120))

                        elif items[i].stat == 2:
                            sy = 8
                            draw.rectangle((x + 1, y, x + sx, y - 177), fill=(255, 50, 0))

                    pic.save('data/pic/P' + tab[0][1:] + 'U' + dbfile[5:-3] + '.png')

        except sqlite3.DatabaseError:
            pass

    # 74x402
    # 74x700
    # 74x1054
    # 74x1352


def mkstat():
    print('\nAnalysing data...\n')
    dir = []
    for (dirpath, dirnames, filenames) in walk('data/db'):
        dir.extend(filenames)
        break

    for dbfile in dir:
        print(dbfile)
        try:
            conn = sqlite3.connect('data/db/' + dbfile)
            stat = [statistic for _ in range(60 * 24)]
            j = 0
            open('data/info/' + dbfile[:-3] + '.vus', 'w', encoding="utf8").write('')
            db = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for tab in db:
                if tab[0][0] == 'T':
                    print(tab[0], ' DONE')
                    items = []
                    try:
                        cursor = conn.execute('SELECT STATE FROM ' + tab[0])
                    except sqlite3.OperationalError:
                        cursor = ''

                    for item in cursor:
                        items.append(item)

                    stat[j].date = str(tab[0][1:])
                    temp = 0
                    all = 0
                    stat[j].maxsd = 0
                    stat[j].minsd = 9223372036854775806
                    for i in range(len(items)):

                        if items[i][0] != 0 and items[i][0] != 2:
                            temp += 1
                            all += 1
                        else:
                            if stat[j].maxsd < temp: stat[j].maxsd = temp
                            if stat[j].minsd > temp and temp != 0: stat[j].minsd = temp
                            temp = 0

                    stat[j].oap = all / len(items) if len(items) != 0 else 0

                    if stat[j].minsd == 9223372036854775806:
                        result = ' 00.00 00 00\n'
                    else:
                        result = ' ' + str(stat[j].oap * 100)[:5] + ' ' + str(stat[j].maxsd) + ' ' + str(
                            stat[j].minsd) + '\n'

                    open('data/info/' + dbfile[:-3] + '.vus', 'a', encoding="utf8").write(stat[j].date + result)
                    j += 1

        except sqlite3.DatabaseError:
            pass


def mkhtml():
    print('\nCombining all parts to html...\n')
    idsdir = []
    for (dirpath, dirnames, filenames) in walk('data/db'):
        idsdir.extend(filenames)
        break

    picdir = []
    for (dirpath, dirnames, filenames) in walk('data/pic'):
        picdir.extend(filenames)
        break

    for ids in idsdir:
        p = person()
        p.user_id = ids[5:-3]
        p.pic = f'profpic_{p.user_id}.jpeg'
        p.profpic = f'data/pic/user_{p.user_id}'
        p.about = json.load(open(f'data/info/user_{p.user_id}.json', 'r'))

        stat = open('data/info/user_' + p.user_id + '.vus', 'r', encoding="utf8")
        # FIXIT

        # info = open('data/info/user_' + p.user_id + '.vui', 'r', encoding="utf8")
        # info = json.load(f'data/info/user_{p.user_id}.json')

        html = open('user_' + p.user_id + '.html', 'w', encoding="utf8")
        example = open('templates/defaultpage.html', 'r', encoding="utf8")
        hat = p.mk_hat(p.about)

        for line in example.readlines():
            if '<!-- %USERDATA% -->\n' in line:
                html.write(hat)
            elif '<!-- %STATDATA% -->\n' in line:
                for stat_line in stat.readlines():
                    element = stat_line.replace('_', ' ').split()
                    day = element[0]
                    mon = element[1]
                    year = element[2]
                    p.oap = element[3]
                    p.maxsd = element[4]
                    p.minsd = element[5]

                    date = day + '/' + mon + '/' + year
                    path = 'P' + day + '_' + mon + '_' + year + 'U' + p.user_id + '.png'
                    alt = date + '_user_' + p.user_id

                    daystat = p.mk_statistic(date=date, path=path, alt=alt)

                    html.write(daystat)
            else:
                html.write(line)
        stat.close()
        html.close()
        example.close()
        print('user_' + p.user_id + '.html', ' DONE')


mkspic()
mkstat()
mkhtml()
print('\nAll data successfully converted to HTML')
