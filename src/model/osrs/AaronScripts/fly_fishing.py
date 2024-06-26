import time

import utilities.color as clr
import utilities.ocr as ocr
from model.osrs.AaronScripts.aaron_functions import AaronFunctions
from utilities.api.morg_http_client import MorgHTTPSocket


class OSRSfishing(AaronFunctions):
    def __init__(self):
        bot_title = "Fishing"
        description = "<Bot description here.>"
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = True

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)

    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):
        api_morg = MorgHTTPSocket()
        starting_exp = api_morg.get_skill_xp(skill="Fishing")
        # Main loop
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            while self.is_fishing():
                self.log_msg("Fishing..")
                if self.activate_special():
                    break
                time.sleep(1)
            if self.search_slot_28():
                self.drop_all(skip_rows=0, skip_slots=[0, 1])
            self.fish()
            time.sleep(5)

            self.update_progress((time.time() - start_time) / end_time)

        ending_exp = api_morg.get_skill_xp(skill="Fishing")
        total_exp_gained = ending_exp - starting_exp
        self.log_msg(f"Gained {total_exp_gained} experience in Fishing")
        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()

    def fish(self):
        counter = 0
        while counter != 10:
            if fishing_spot := self.get_nearest_tag(color=clr.CYAN):
                self.mouse.move_to(fishing_spot.random_point())
                if not self.mouseover_text(contains="Use", color=clr.OFF_WHITE):
                    continue
                self.mouse.click()
                break
            counter += 1
            
    def is_fishing(self):
        if ocr.find_text("Fishing", self.win.game_view, ocr.PLAIN_12, clr.GREEN):
            return True
        else:
            self.log_msg("Could not find fishing text")