import time

import utilities.color as clr
import utilities.imagesearch as imsearch
import pyautogui as pag
import utilities.ocr as ocr
from model.osrs.AaronScripts.aaron_functions import AaronFunctions

class OSRSpotionmaker(AaronFunctions):
    def __init__(self):
        bot_title = "Potion Maker"
        description = "<Bot description here.>"
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = 1
        self.potion_list = ['Super Combats', 'Prayer', 'Super Restore', 'Anti-Venom +']

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_dropdown_option("potion_to_make", "Select potion", self.potion_list)
        
    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "potion_to_make":
                self.potion_to_make = options[option]
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):

        # Main loop
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:             
            self.open_bank_super_cmbs()
            self.make_potions_super_cmbs()
            
            # self.open_bank()
            # self.make_potions()           
            
            self.update_progress((time.time() - start_time) / end_time)

        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()
    
    def get_primary_bank_img(self):
        if self.potion_to_make == 'Prayer':
            primary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "ranarr_potion_(unf)_bank.png")
        elif self.potion_to_make == 'Super Restore':
            primary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "snapdragon_potion_(unf)_bank.png")
        elif self.potion_to_make == 'Anti-Venom +':
            primary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "anti-venom(4)_bank.png")
        return primary_bank_img
    
    def get_secondary_bank_img(self):
        if self.potion_to_make == 'Prayer':
            secondary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "snape_grass_bank.png")
        elif self.potion_to_make == 'Super Restore':
            secondary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "red_spiders'_eggs_bank.png")
        elif self.potion_to_make == 'Anti-Venom +':
            secondary_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "torstol_bank.png")

        return secondary_bank_img 
    
    def make_potions(self):
        primary_bank_img = self.get_primary_bank_img() 
        secondary_bank_img = self.get_secondary_bank_img() 
        if secondary := self.wait_until_img(secondary_bank_img, self.win.control_panel):
            self.log_msg("Secondary found in inventory")
            self.mouse.move_to(secondary.random_point())
            self.mouse.click()
        else:
            self.log_msg("Secondary was not found in inventory. Stopping script.")
            
        if primary := self.wait_until_img(primary_bank_img, self.win.control_panel):
            self.log_msg("Primary found in inventory")
            self.mouse.move_to(primary.random_point())
            self.mouse.click()
        else:
            self.log_msg("Primary was not found in inventory. Stopping script.")
            
        time.sleep(1)
        pag.press('space')
        time.sleep(5) # Guarantees that if the last message  was amulet breaking, we don't start everything
        counter = 0
        while counter <= 10: # Usually 17 seconds but minus 1 for the above sleep(1)
            if self.chatbox_text_RED_dodgy_necklace(contains="crumbles"):
                self.log_msg("Amulet broken. Banking.")
                break
            counter += 1
            time.sleep(1)
            
    def make_potions_super_cmbs(self):
        torst_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "torstol_bank.png")
        super_str_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "super_strength(4)_bank.png")
        if torst_bank := self.wait_until_img(torst_bank_img, self.win.control_panel):
            self.log_msg("Torstol found in inventory")
            self.mouse.move_to(torst_bank.random_point())
            self.mouse.click()
        else:
            self.log_msg("Torstol was not found in inventory. Stopping script.")
            
        if super_str := self.wait_until_img(super_str_bank_img, self.win.control_panel):
            self.log_msg("Secondary found in inventory")
            self.mouse.move_to(super_str.random_point())
            self.mouse.click()
        else:
            self.log_msg("Super strength was not found in inventory. Stopping script.")
        time.sleep(1)
        pag.press('space')
        time.sleep(8.5)
            
    def check_broken_amulet_text(self):
        amulet_of_chemistry_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "amulet_of_chemistry_bank.png")
        amulet_of_chemistry_bank = imsearch.search_img_in_rect(amulet_of_chemistry_bank_img, self.win.game_view)
        if self.chatbox_text_RED_dodgy_necklace(contains="crumbles"):
            self.log_msg("Broken amulet text found in chat")
            self.mouse.move_to(amulet_of_chemistry_bank.random_point())
            self.mouse.right_click()
            if withdraw_text := ocr.find_text("1 Amulet", self.win.game_view, ocr.BOLD_12, [clr.WHITE, clr.ORANGE]):
                self.mouse.move_to(withdraw_text[1].random_point(), knotsCount=0)
                self.log_msg("Withdrawing new amulet")
                self.mouse.click()
                time.sleep(1)
        amulet_of_chemistry_inv_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "amulet_of_chemistry.png")
        if amulet_of_chemistry_inv := imsearch.search_img_in_rect(amulet_of_chemistry_inv_img, self.win.control_panel):
            self.mouse.move_to(amulet_of_chemistry_inv.random_point())
            pag.keyDown('shift')
            self.mouse.click()
            pag.keyUp('shift')
            self.log_msg("Amulet equipped successfully")
            time.sleep(1)
        return
        
        
    def open_bank(self):
        self.open_bank_af() # Click banker
        primary_bank = self.get_primary_bank_img() 
        secondary_bank = self.get_secondary_bank_img() 
        self.deposit_all()
        self.check_broken_amulet_text()
        if primary := imsearch.search_img_in_rect(primary_bank, self.win.game_view):
            if secondary := imsearch.search_img_in_rect(secondary_bank, self.win.game_view):
                self.log_msg("Found primary in bank view")
                self.mouse.move_to(primary.random_point())
                if self.mouseover_text(contains="Release"):
                    self.log_msg("Ran out of primary. Stopping script.")
                    self.stop()
                self.mouse.click()
                self.log_msg("Found secondary in bank view")
                self.mouse.move_to(secondary.random_point())
                if self.mouseover_text(contains="Release"):
                    self.log_msg("Ran out of secondary. Stopping script.")
                    self.stop()
                self.mouse.click()
            else:
                self.log_msg("Ran out of primary. Stopping script.")
                self.stop()           
        else:
            self.log_msg("Ran out of secondary. Stopping script.")
            self.stop()      
        while not self.search_slot_28():
            time.sleep(0.5)
        self.log_msg("Exiting bank.") 
        pag.press("escape")
        
    def open_bank_super_cmbs(self):
        self.open_bank_af() # Click banker
        torst_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "torstol_bank.png")
        super_str_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "super_strength(4)_bank.png")
        super_atk_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "super_attack(4)_bank.png")
        super_def_bank_img = imsearch.BOT_IMAGES.joinpath("Aarons_images", "super_defence(4)_bank.png")
        self.deposit_all()
        if torst_bank := imsearch.search_img_in_rect(torst_bank_img, self.win.game_view):
            self.log_msg("Deposit button successfully clicked.")
            self.mouse.move_to(torst_bank.random_point())
            if self.mouseover_text(contains="Release"):
                self.log_msg("Ran out of torstols. Stopping script.")
                self.stop()
            self.mouse.click()
        else:
            self.log_msg("Ran out of torstols. Stopping script.")
            self.stop()
            
        if super_str_bank := imsearch.search_img_in_rect(super_str_bank_img, self.win.game_view):
            self.log_msg("Deposit button successfully clicked.")
            self.mouse.move_to(super_str_bank.random_point())
            if self.mouseover_text(contains="Release"):
                self.log_msg("Ran out of torstols. Stopping script.")
                self.stop()
            self.mouse.click()
        else:
            self.log_msg("Ran out of super strengths. Stopping script.")
            self.stop()
            
        if super_atk_bank := imsearch.search_img_in_rect(super_atk_bank_img, self.win.game_view):
            self.log_msg("Deposit button successfully clicked.")
            self.mouse.move_to(super_atk_bank.random_point())
            if self.mouseover_text(contains="Release"):
                self.log_msg("Ran out of torstols. Stopping script.")
                self.stop()
            self.mouse.click()
        else:
            self.log_msg("Ran out of super attacks. Stopping script.")
            self.stop()
            
        if super_def_bank := imsearch.search_img_in_rect(super_def_bank_img, self.win.game_view):
            self.log_msg("Deposit button successfully clicked.")
            self.mouse.move_to(super_def_bank.random_point())
            if self.mouseover_text(contains="Release"):
                self.log_msg("Ran out of torstols. Stopping script.")
                self.stop()
            self.mouse.click()
        else:
            self.log_msg("Ran out of super defences. Stopping script.")
            self.stop()
  
        while not self.search_slot_28():
            time.sleep(0.5)
        self.log_msg("Exiting bank.") 
        pag.press("escape")