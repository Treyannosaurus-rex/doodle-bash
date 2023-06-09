import pygame

class Wizard():
    def __init__ (self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #| 0: idle | 1: run/movement | 2: attack_1 | 3: attack_2 | 4: jump | 5: hit | 6: die
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.jump_cooldown = 0
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        #print(animation_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get kepresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True:            
            #movement
            if key[pygame.K_j]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_l]:
                dx = SPEED
                self.running = True
            #jump
            if key[pygame.K_i] and not self.jump and self.jump_cooldown == 0:
                self.vel_y = -25
                self.jump = True
                self.jump_cooldown = 40 #frames of cooldown
            #attack
            if key[pygame.K_r] or key[pygame.K_e]:
                self.attack(surface, target)
                #determine which attack type was used
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_e]:
                    self.attack_type = 2
        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 189:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 189 - self.rect.bottom

        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #update player position
        self.rect.x += dx
        self.rect.y += dy

        #update jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    #handle animation updates
    def update(self):
        #check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #die
        elif self.hit == True:
            self.update_action(5) #hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(2) #attack_1
            elif self.attack_type == 2:
                self.update_action(3) #attack_2
        elif self.jump == True:
            self.update_action(4) #jump
        elif self.running == True:
            self.update_action(1) #run
        else:
            self.update_action(0) #idle

        animation_cooldown = 100 #milsecs
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead; if so, end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if an attack was executed
                if self.action == 2 or self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 20
                #check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #if player is in the middle of an attack, the attacks clank and attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                #print("HIT!")
                target.health -= 10
                target.hit = True
        
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        #check if the new action is different than the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] *self.image_scale), self.rect.y - (self.offset[1] *self.image_scale)))
