import pygame
import math
import heapq
from collections import defaultdict
import random
class hero:
    obstacles = []
    def __init__(self):
        self.hp=100
        self.stat=True
        self.regen=1/FPS
        self.xpos=1560
        self.ypos=1380
        
        self.x_boost=0
        self.y_boost=0
        self.angle=0
        self.angle_boost=0
        self.speed=300
        self.angle_s=5
        
        self.image_hero=pygame.image.load(r"C:\Users\MSI\Desktop\Hero1.png")
        self.image_hero=pygame.transform.scale(self.image_hero, (100, 50))
        self.image_hero_true=self.image_hero
        self.cord_hero=self.image_hero_true.get_rect()
        self.cord_hero= self.image_hero.get_rect()
        self.cord_hero.center=(self.xpos,self.ypos)
        self.flag_angle=0
        self.flag_x=0
        self.flag_y=0
    def check_collision(self, rect_to_check,enemys):
        """Проверяет коллизии с препятствиями и другими врагами"""
        # Проверка с препятствиями
        for obstacle in self.__class__.obstacles:
            if rect_to_check.colliderect(obstacle.rect):
                return True
            # Проверка с другими врагами
        for enemy in enemys:
            if rect_to_check.colliderect(enemy.collision_rect):
                return True
        return False
    def take_damage(self,amount):
        self.hp -= amount
        return self.hp <= 0
        
    def move(self,enemy):
        if self.stat:
            if self.hp<100:
                self.hp+=self.regen
            self.xlast=self.xpos
            self.ylast=self.ypos
            self.xboostlast=self.x_boost
            self.yboostlast=self.y_boost
            key_get=pygame.key.get_pressed()
            if key_get[pygame.K_a] or (self.angle_boost!=0 and (not(key_get[pygame.K_d])) and self.flag_angle==1):
                self.angle+=self.angle_s*self.angle_boost
                self.flag_angle=1
                if abs(self.angle_boost)<2 and key_get[pygame.K_a]:
                    if self.angle_boost<0:
                        self.angle_boost+=0.03
                    else:
                        self.angle_boost+=0.01
                elif self.angle_boost>0:
                    self.angle_boost-=0.02
                else:
                    self.angle_boost=0
                self.image_hero_true= pygame.transform.rotozoom(self.image_hero, self.angle,1)
                
            if key_get[pygame.K_d] or (self.angle_boost!=0 and (not(key_get[pygame.K_a])) and self.flag_angle==2):
                self.angle+=self.angle_s*self.angle_boost
                self.flag_angle=2
                if abs(self.angle_boost)<2 and key_get[pygame.K_d]:
                    if self.angle_boost>0:
                        self.angle_boost-=0.03
                    else:
                        self.angle_boost-=0.01
                elif self.angle_boost<0 :
                    self.angle_boost+=0.02
                else:
                    self.angle_boost=0
                self.image_hero_true= pygame.transform.rotozoom(self.image_hero, self.angle,1)
            if (key_get[pygame.K_LEFT] and not(key_get[pygame.K_RIGHT]))  or (self.x_boost<0 and (not(key_get[pygame.K_RIGHT])) and self.flag_x==1):
                self.flag_x=1
                if abs(self.x_boost)<2 and key_get[pygame.K_LEFT]:
                    if self.x_boost>0:
                        self.x_boost-=0.03
                    else:
                        self.x_boost-=0.03
                elif self.x_boost <-0.03:
                    self.x_boost+=0.02
                else:
                    self.x_boost=0
                
            if (key_get[pygame.K_RIGHT] and not(key_get[pygame.K_LEFT])) or (self.x_boost>0 and (not(key_get[pygame.K_LEFT])) and self.flag_x==2):
                self.flag_x=2
                if abs(self.x_boost)<2 and key_get[pygame.K_RIGHT]:
                    if self.x_boost>0:
                        self.x_boost+=0.03
                    else:
                        self.x_boost+=0.03
                elif self.x_boost >0.03:
                    self.x_boost-=0.02
                else:
                    self.x_boost=0
            if self.x_boost!=0:
                self.xpos=self.xpos+(self.speed/FPS)*self.x_boost
                if key_get[pygame.K_RIGHT] and key_get[pygame.K_LEFT]:
                    if self.x_boost>0.03:
                        self.x_boost-=0.03
                    elif self.x_boost<-0.03:
                        self.x_boost+=0.03
                    else:
                        self.x_boost=0
            if (key_get[pygame.K_UP] and not(key_get[pygame.K_DOWN]))  or (self.y_boost<0 and (not(key_get[pygame.K_DOWN])) and self.flag_y==1):
                self.flag_y=1
                if abs(self.y_boost)<2 and key_get[pygame.K_UP]:
                    if self.y_boost>0:
                        self.y_boost-=0.03
                    else:
                        self.y_boost-=0.03
                elif self.y_boost <-0.03:
                    self.y_boost+=0.02
                else:
                    self.y_boost=0
                
            if (key_get[pygame.K_DOWN] and not(key_get[pygame.K_UP])) or (self.y_boost>0 and (not(key_get[pygame.K_UP])) and self.flag_y==2):
                self.flag_y=2
                if abs(self.y_boost)<2 and key_get[pygame.K_DOWN]:
                    if self.y_boost>0:
                        self.y_boost+=0.03
                    else:
                        self.y_boost+=0.03
                elif self.y_boost >0.03:
                    self.y_boost-=0.02
                else:
                    self.y_boost=0
            if self.y_boost!=0:
                self.ypos=self.ypos+(self.speed/FPS)*self.y_boost
                if key_get[pygame.K_UP] and key_get[pygame.K_DOWN]:
                    if self.y_boost>0.03:
                        self.y_boost-=0.03
                    elif self.y_boost<-0.03:
                        self.y_boost+=0.03
                    else:
                        self.y_boost=0
            self.cord_hero= self.image_hero_true.get_rect()
            self.cord_hero.center=(self.xpos,self.ypos)
            if not self.check_collision(self.cord_hero,enemy):
                rotated_rect = self.image_hero_true.get_rect(center=self.cord_hero.center)
            else:
                self.xpos=self.xlast
                self.ypos=self.ylast
                self.x_boost=-self.x_boost/10
                self.y_boost=-self.y_boost/10
                self.cord_hero.center=(self.xpos,self.ypos)
                rotated_rect = self.image_hero_true.get_rect(center=self.cord_hero.center)
            

        
        
        
class Bullet:
    def __init__(self,x_bullet,y_bullet,angle_bullet,damage=100,speed_bullet=30):
        self.image=pygame.transform.scale(pygame.image.load(r"C:\Users\MSI\Desktop\byllet.png"), (10, 10))
        self.x=x_bullet
        self.y=y_bullet
        self.angle=angle_bullet
        self.damage=damage
        self.x_speed=math.cos(math.radians(self.angle))
        self.y_speed=-math.sin(math.radians(self.angle))
        self.speed_bullet=speed_bullet
        self.rect = self.image.get_rect(center=(x_bullet, y_bullet))
    def update(self):
        self.x=self.x_speed*self.speed_bullet+self.x
        self.y=self.y_speed*self.speed_bullet+self.y
        self.rect.center = ((self.x), (self.y))
    def draw(self):
        
        rotated_image = pygame.transform.rotozoom(self.image,self.angle,1)
        screen.blit(rotated_image, rotated_image.get_rect(center=self.rect.center))
        
class Bullet_Enemy:
    def __init__(self,x_bullet,y_bullet,angle_bullet,damage=10,speed_bullet=30):
        self.image=pygame.transform.scale(pygame.image.load(r"C:\Users\MSI\Desktop\byllet.png"), (10, 10))
        self.x=x_bullet
        self.y=y_bullet
        self.angle=angle_bullet
        self.damage=damage
        self.x_speed=math.cos(math.radians(self.angle))
        self.y_speed=-math.sin(math.radians(self.angle))
        self.speed_bullet=speed_bullet
        self.rect = self.image.get_rect(center=(x_bullet, y_bullet))
    def update(self):
        self.x=self.x_speed*self.speed_bullet+self.x
        self.y=self.y_speed*self.speed_bullet+self.y
        self.rect.center = ((self.x), (self.y))
    def draw(self):
        rotated_image = pygame.transform.rotozoom(self.image,self.angle,1)
        screen.blit(rotated_image, rotated_image.get_rect(center=self.rect.center))


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (100, 100, 100, 200), (0, 0, width, height))

        
class Enemy:
    all_enemies = []
    shared_path = []
    obstacles = []
    collision_radius = 50  # Радиус для избегания столкновений
    path_graph = {}  # Граф связей между точками


    
    def __init__(self,i):
        self.image = pygame.transform.scale(pygame.image.load(r"C:\Users\MSI\Desktop\vrag2.png"), (100, 100))
        self.current_point_index = i
        self.rect = self.image.get_rect(center=self.shared_path[self.current_point_index])
        self.speed = 2
        self.angle = 0
        self.hp=100
        self.path = []
        self.cooldawn=0
        self.__class__.all_enemies.append(self)
        self.collision_rect = pygame.Rect(200, 200, self.collision_radius, self.collision_radius)
        self.update_collision_rect()
        self.stuck_timer = 0  # Таймер для решения проблемы застревания

    def update_collision_rect(self):
        """Обновляет прямоугольник коллизий"""
        self.collision_rect.center = self.rect.center

    def check_collision(self, rect_to_check,player):
        """Проверяет коллизии с препятствиями и другими врагами"""
        # Проверка с препятствиями
        for obstacle in self.__class__.obstacles:
            if rect_to_check.colliderect(obstacle.rect):
                return True
        # Проверка с другими врагами
        for enemy in self.__class__.all_enemies:
            if enemy != self and rect_to_check.colliderect(enemy.collision_rect):
                return True
        if rect_to_check.colliderect(player):
            return True
                
        return False
    
    def find_safe_move(self, target_pos,player):
        """Находит безопасное направление движения"""
        base_dx = target_pos[0] - self.rect.centerx
        base_dy = target_pos[1] - self.rect.centery
        distance = math.hypot(base_dx, base_dy)
        if distance == 0:
            return 0, 0
        
        # Нормализованный вектор направления
        base_dx /= distance
        base_dy /= distance
        
        # Пробуем разные варианты движения
        for attempt in range(10):
            if attempt == 0:
                # Прямое движение к цели
                dx, dy = base_dx, base_dy
            else:
                # Добавляем случайное отклонение
                angle = math.radians(attempt * 30 * (1 if attempt % 2 else -1))
                dx = base_dx * math.cos(angle) - base_dy * math.sin(angle)
                dy = base_dx * math.sin(angle) + base_dy * math.cos(angle)
            
            # Рассчитываем новую позицию
            move_x = dx * self.speed
            move_y = dy * self.speed
            new_rect = self.collision_rect.copy()
            new_rect.x += move_x
            new_rect.y += move_y
            
            if not self.check_collision(new_rect,player):
                return move_x, move_y
        
        # Если не нашли безопасный путь, стоим на месте
        return 0, 0

    def move_towards(self, target_pos,player):
        """Плавное движение с обходом препятствий"""
        # Если застряли, увеличиваем таймер
        if math.dist(self.rect.center, target_pos) < 5:
            self.stuck_timer += 1
            
        else:
            self.stuck_timer = 0
        # Если застряли надолго, пытаемся "выбраться"
        if self.stuck_timer > 60 :  # 1 секунда при 60 FPS
            escape_x = (random.random() - 0.5) * self.speed * 2
            escape_y = (random.random() - 0.5) * self.speed * 2 
            new_rect = self.collision_rect.copy()
            new_rect.x += escape_x
            new_rect.y += escape_y
            if not self.check_collision(new_rect,player):
                self.rect.x += escape_x
                self.rect.y += escape_y
                self.update_collision_rect()
                return
       
        # Обычное движение
        move_x, move_y = self.find_safe_move(target_pos,player)
        self.rect.x += move_x
        self.rect.y += move_y
        self.update_collision_rect()

    def update(self, player_pos,player):
        # Находим ближайшую к игроку точку
        closest_idx = min(
            range(len(self.shared_path)),
            key=lambda i: math.dist(self.shared_path[i], player_pos)
        )
        
        # Обновляем путь только если цель изменилась
        if not self.path or self.path[-1] != closest_idx:
            self.path = [closest_idx]
        # Двигаемся по пути
        if self.path:
            target_pos = self.shared_path[self.path[0]]
            self.move_towards(target_pos,player)
            
            # Проверяем достижение точки
            if math.dist(self.rect.center, target_pos) < 15:
                self.current_point_index = self.path[0]
                self.path.pop(0)

        
        # Плавный поворот к игроку
        px, py = player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        target_angle = math.degrees(math.atan2(-dy, dx))
        
        # Плавное изменение угла
        angle_diff = (target_angle - self.angle + 180) % 360 - 180
        self.angle += angle_diff * 0.1  # Коэффициент плавности поворота
        dist=math.sqrt((self.rect.centerx - px)**2 + (self.rect.centery - py)**2)
        if dist<=1000:
            self.shot()
    def draw(self, surface):
        rotated = pygame.transform.rotozoom(self.image, self.angle,1)
        surface.blit(rotated, rotated.get_rect(center=self.rect.center))
    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0
    def shot(self):
        if self.cooldawn<=0:
            new=Bullet_Enemy(self.rect.centerx,self.rect.centery,self.angle)
            bullets_enemy.append(new)
            self.cooldawn=1*FPS
        if self.cooldawn>0:
            self.cooldawn-=1
class Camera:
    def __init__(self, screen_width, screen_height, world_width=2000, world_height=2000):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        
    def apply(self, entity):
        """Преобразует мировые координаты в экранные"""
        if isinstance(entity, pygame.Rect):
            return entity.move(-self.camera.x, -self.camera.y)
        elif hasattr(entity, 'rect'):
            return entity.rect.move(-self.camera.x, -self.camera.y)
        elif isinstance(entity, (tuple, list)):
            return (entity[0] - self.camera.x, entity[1] - self.camera.y)
        return entity
    
    def update(self, target):
        """Центрирует камеру на цели с учетом границ мира"""
        # Центрируем камеру на цели
        x = target.cord_hero.centerx - self.screen_width // 2
        y = target.cord_hero.centery - self.screen_height // 2
        
        # Ограничиваем камеру границами мира
        x = max(0, min(x, self.world_width - self.screen_width))
        y = max(0, min(y, self.world_height - self.screen_height))
        
        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)
        
    def draw(self, surface, image, rect):
        """Отрисовывает изображение с учетом позиции камеры"""
        surface.blit(image, self.apply(rect))

WIDTH = 1200
HEIGHT = 800
FPS = 60

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создаем камеру (размеры мира могут быть больше экрана)
WORLD_WIDTH, WORLD_HEIGHT = 3000, 3000
camera = Camera(WIDTH, HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

# Создаем героя
gg = hero()

# Создаем препятствия (как в вашем коде)
Obstacle.obstacles = [
    Obstacle(300, 600, 180, 1013),
    Obstacle(300, 600, 1153, 145),
    Obstacle(1425, 15, 28, 585),
    Obstacle(1425, 15, 313, 328),
    Obstacle(1738,15, 144, 40),
    Obstacle(1844,15, 40, 730),
    Obstacle(1136,750, 132, 131),
    Obstacle(1136,735, 445, 35),
    Obstacle(1738,735, 629, 35),
    Obstacle(2339,465, 28, 270),
    Obstacle(2339,465, 615, 25),
    Obstacle(2908,492, 42, 1538),
    Obstacle(2339,465, 615, 25),
    Obstacle(1826,1991, 1082, 36),
    Obstacle(1826,1991, 40, 981),
    Obstacle(171,1576, 1098, 37),
    Obstacle(171,1576, 102, 436),
    Obstacle(272,1978, 212, 1010),
    Obstacle(480,2931, 1350, 35),
    Obstacle(480,1259, 789, 319),
    Obstacle(887,1111, 382, 149),
    Obstacle(1135,1028, 134, 84),
    Obstacle(798,1977, 110, 586),
    Obstacle(443,1831, 41, 147),
    Obstacle(900,1977, 56, 37),
    Obstacle(900,2526, 56, 37),
    Obstacle(1111,1977, 159, 37),
    Obstacle(1227,2014, 43, 549),
    Obstacle(1111,2525, 117, 38),
    Obstacle(2366,736, 110, 35),
    Obstacle(2659,736, 250, 35),
    Obstacle(1267,1173, 433, 37),
    Obstacle(1856,1173, 276, 443),
    Obstacle(1385,1578, 472, 37),
    Obstacle(2300,1212, 272, 231),
    Obstacle(2491,1442, 236, 211),
    Obstacle(2491,1000, 236, 215),
    Obstacle(272,1610, 126, 76),
    Obstacle(480,2417, 80, 279),
    Obstacle(600,2848, 415, 90),
    Obstacle(633,1610, 342, 73),
    Obstacle(1726,1614, 131, 163),
    Obstacle(2159,1905, 552, 90),
    Obstacle(1935,765, 173, 64),
    Obstacle(1710,2377, 120, 223),
    Obstacle(1260,1208, 362, 69),
    Obstacle(1260,1208, 80, 170),
    Obstacle(1677,1514, 200, 70),
]
Enemy.obstacles = Obstacle.obstacles
hero.obstacles = Obstacle.obstacles
obstacles = Obstacle.obstacles

mapimage=pygame.transform.scale(pygame.image.load(r"C:\Users\MSI\Desktop\map.jpg"), (3000, 3000))
maprect=mapimage.get_rect()

 


# Создаем врагов
Enemy.shared_path = [
    (570, 860), (570, 1160), 
    (800, 1160), (800, 860),
    (1030, 960), (1200, 960),
    (1400, 960), (1784, 960),
    (1650,754),(1650, 484),
    (1790, 484),(1776, 1200),
    (1715, 1393),(1320, 1466),
    (1320, 1600),(2193,995),
    (2561, 863),(2803, 900),
    (2564, 590),(2803, 1329),
    (2800, 1800),(2188, 1797),
    (1830, 1895),(1660, 1900),
    (1658, 2296),(1473, 2315),
    (1416, 2745),(1638, 2745),
    (570, 860),(1000, 2741),
    (1010, 2450),(1010, 2164),
    (1024, 2004),(1027, 1835),
    (610, 1835),(610, 2163),
    (637,  2674),(626, 2412),
    (450, 1731),
]
enemies = [Enemy(random.randint(0,len(Enemy.shared_path)-1)) for _ in range(5)]

# Игровые переменные
bullets = []
bullets_enemy = []
cooldawn = 0
timespawn = 0
ochki = 0
timetoochki = FPS
ran = True
timetoivent=0
iventflag=0
zontotace=0
iventhave=True
iventrect=pygame.Rect(0,0,0,0)
iventimage = pygame.Surface((0, 0), pygame.SRCALPHA)
take=FPS*10
# Основной игровой цикл
while ran:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ran = False
    
    # Обновляем камеру (должно быть ПЕРЕД всеми движениями)
    camera.update(gg)

    # Обновляем игрока
    key_get = pygame.key.get_pressed()
    
    # Обновляем врагов
    for enemy in enemies:
        enemy.update(gg.cord_hero.center, gg.cord_hero)
    # Обработка выстрелов
    if key_get[pygame.K_SPACE] and cooldawn <= 0:
        new = Bullet(gg.xpos, gg.ypos, gg.angle)
        bullets.append(new)
        cooldawn = 0.25 * FPS
    if cooldawn > 0:
        cooldawn -= 1
    
    # Спавн врагов
    if len(enemies) <= 20 and timespawn <= 0:
        for kol in range(3):
            enemies.append(Enemy(random.randint(0,len(Enemy.shared_path)-1)))
        timespawn = FPS * 5
    else:
        timespawn -= 1
    
    # Обновление пуль
    for bullet in bullets_enemy[:]:
        bullet.update()
        if not (0 <= bullet.x <= WORLD_WIDTH and 0 <= bullet.y <= WORLD_HEIGHT):
            bullets_enemy.remove(bullet)
        for obstacle in obstacles:
            if bullet.rect.colliderect(obstacle.rect):
                bullets_enemy.remove(bullet)
                break
        if bullet.rect.colliderect(gg.cord_hero):
            if gg.take_damage(bullet.damage):
                gg.stat = False
                
            bullets_enemy.remove(bullet)
    
    for bullet in bullets[:]:
        bullet.update()
        if not (0 <= bullet.x <= WORLD_WIDTH and 0 <= bullet.y <= WORLD_HEIGHT):
            bullets.remove(bullet)
        for obstacle in obstacles:
            if bullet.rect.colliderect(obstacle.rect):
                bullets.remove(bullet)
                break
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                if enemy.take_damage(bullet.damage):
                    enemies.remove(enemy)
                    Enemy.all_enemies.remove(enemy)
                    ochki += 10
                bullets.remove(bullet)
                break
    
    # Обновление очков
    if timetoochki <= 0 and gg.stat:
        ochki += 1
        timetoochki = FPS
    else:
        timetoochki -= 1
        
    if timetoivent<=0 and iventflag==0:
        ivent=random.randint(0,3)
        timetoivent=FPS*10
        if ivent!=0:
            iventflag=1
            iventhave=True
    if timetoivent>0 and iventflag==0:
        timetoivent-=1
    if ivent==1 and iventhave:
        iventrect = pygame.Rect(2654, 575, 201, 116)
        iventimage = pygame.Surface((201, 116), pygame.SRCALPHA)
        pygame.draw.rect(iventimage, (200, 0, 0, 200), (0, 0, 201, 116))
        iventhave=False
    elif ivent==2 and iventhave:
        iventrect = pygame.Rect(570, 892, 116, 242)
        iventimage = pygame.Surface((116, 242), pygame.SRCALPHA)
        pygame.draw.rect(iventimage, (200, 0, 0, 200), (0, 0, 116, 242))
        iventhave=False
    elif ivent==3 and iventhave:
        iventrect = pygame.Rect(320, 1716, 106, 80)
        iventimage = pygame.Surface((106, 80), pygame.SRCALPHA)
        pygame.draw.rect(iventimage, (200, 0,0, 200), (0, 0, 106, 80))
        iventhave=False
    if ivent!=0:
        if iventrect.colliderect(gg.cord_hero):
            take-=1
            if take<=0 and gg.stat:
                ochki+=100
                take=FPS*10
                ivent=0
                iventflag=0
                timetoivent=FPS*10
        else:
            take=FPS*10

    
    # Отрисовка
    
    screen.fill("black")
    # Отрисовка объектов через камеру
    camera.draw(screen, mapimage, maprect)
    for obstacle in obstacles:
        camera.draw(screen, obstacle.image, obstacle.rect)
    
    for bullet in bullets_enemy:
        rotated_image = pygame.transform.rotozoom(bullet.image, bullet.angle, 1)
        camera.draw(screen, rotated_image, rotated_image.get_rect(center=bullet.rect.center))
    
    for bullet in bullets:
        rotated_image = pygame.transform.rotozoom(bullet.image, bullet.angle, 1)
        camera.draw(screen, rotated_image, rotated_image.get_rect(center=bullet.rect.center))
    
    for enemy in enemies:
        rotated = pygame.transform.rotozoom(enemy.image, enemy.angle, 1)
        camera.draw(screen, rotated, rotated.get_rect(center=enemy.rect.center))
    if iventflag==1:
        camera.draw(screen, iventimage, iventrect)
    # Отрисовка героя
    rotated_hero = pygame.transform.rotozoom(gg.image_hero, gg.angle, 1)
    camera.draw(screen, rotated_hero, rotated_hero.get_rect(center=gg.cord_hero.center))
    hep = pygame.font.Font(None, 36)
    text_hep = hep.render(f'ОЧКИ: {gg.hp:.0f}', True, 'green')
    screen.blit(text_hep, (50, 50))
    # Отрисовка очков (в экранных координатах)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f'ОЧКИ: {ochki}', True, 'red')
    screen.blit(text_surface, (WIDTH//2 - 100, 50))
    enemy_col=Enemy.all_enemies
    gg.move(enemy_col)
    if not gg.stat:
        font = pygame.font.Font(None, 100)
        text_surface = font.render(f'вы проиграли', True, 'red')
        screen.blit(text_surface, (WIDTH//2-250 , HEIGHT//2-100))
    pygame.display.flip()
    clock.tick(FPS)
    
    
pygame.quit()

        

