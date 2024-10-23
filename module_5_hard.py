import time

# "Свой YouTube"
# Классы (User, Video, UrTube для взаимодействия с платформой, каждый из которых будет содержать
# методы добавления видео, авторизации и регистрации пользователя и т.д.

class User:
    '''
    Класс User необходим для авторизации и регистрации пользователя.
    Атрибуты: nickname(имя пользователя, строка),
              password(в хэшированном виде, число),
              age(возраст, число)
    '''
    def __init__(self, nickname, password, age):
        self.nickname = str(nickname)
        self.password = hash(password)
        self.age = int(age)

    def __str__(self):
       return str(f'{self.nickname}')

class Video:
    '''
    Класс Video необходим для добавления видео
    Атрибуты: title(заголовок, строка), duration(продолжительность, секунды),
              time_now(секунда остановки (изначально 0)),
              adult_mode(ограничение по возрасту,
              bool (False по умолчанию))
    '''
    def __init__(self, title, duration, adult_mode = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __contains__(self, word_to_search):
        if str(word_to_search).lower() in str(self.title).lower():
            return True
        return False


class UrTube:
    '''
    Атрибуты: users(список объектов User), videos(список объектов Video),
              current_user(текущий пользователь, User)
    Методы: log_in - принимает на вход аргументы: nickname, password и пытается найти пользователя в
                 users с такими же логином и паролем. Если такой пользователь существует, то
                 current_user меняется на найденного. password сравнивается по хэшу.
            register - принимает три аргумента: nickname, password, age, и добавляет пользователя в
                   список, если пользователя не существует (с таким же nickname). Если существует,
                   выводит на экран: "Пользователь {nickname} уже существует". После регистрации,
                   вход выполняется автоматически.
            log_out - для сброса текущего пользователя на None.
            add - принимает неограниченное кол-во объектов класса Video и все добавляет в videos,
              если с таким же названием видео ещё не существует. В противном случае ничего не
              происходит.
            get_videos - принимает поисковое слово и возвращает список названий всех видео,
                     содержащих поисковое слово. Следует учесть, что слово 'UrbaN' присутствует
                     в строке 'Urban the best' (не учитывать регистр).
            watch_video - принимает название фильма, если не находит точного совпадения(вплоть до
                        пробела), то ничего не воспроизводится, если же находит - ведётся отчёт в консоль на
                        какой секунде ведётся просмотр. После текущее время просмотра
                        данного видео сбрасывается.
    '''
    users = {}
    videos = {}
    current_user = None

    def register(self, nickname, password, age):
        if  nickname not in self.users:
            new_user = User(nickname, password, age)
            self.users[nickname] = new_user
            self.current_user = new_user
        else:
            print(f"Пользователь {nickname} уже существует")

    def log_in(self, nickname, password):
        if nickname in self.users and hash(password) == self.users[nickname].password:
            #print(f'Текущим пользователем становится {nickname}')
            self.current_user = self.users[nickname]
        else:
            print(f"Либо {nickname} нет в базе, либо неверный пароль!")

    def log_out(self):
        print(f'Текущим пользователем был: {self.current_user.nickname}')
        self.current_user = None

    def add(self, *args):
        for video in args:
            if video.title not in self.videos:
                #print(f'Добавляем видео {video.title}')
                self.videos[video.title] = video
            else:
                print(f'Видео {video.title} уже есть!')

    def get_videos(self, word_to_search):
        video_list = []
        for video_obj in self.videos.values():
            if word_to_search in video_obj:
                video_list.append(video_obj.title)
        return video_list

    def watch_video(self, video_name):
        if self.current_user == None:
            print('Войдите в аккаунт, чтобы смотреть видео')
        elif video_name not in self.videos:
            print('Указанный фильм не найден')
        elif self.videos[video_name].adult_mode and self.current_user.age < 18:
            print('Вам нет 18 лет, пожалуйста, покиньте страницу')
        else: # просмотр видео
            out_str = ''
            for sec in range(1, self.videos[video_name].duration + 1):
                time.sleep(1)
                out_str += str(sec) + ' '
                self.videos[video_name].time_now = sec
            print(out_str + 'Конец видео')
            self.videos[video_name].time_now = 0


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

#Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
