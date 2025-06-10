import customtkinter as ctk
from src.main.persistance.Supabase import DatabaseConfig
from src.main.config.logger_config import log
from main.config.SitesConfigLoader import ConfigLoader
from src.main.service.ScraperService import ScraperService
from src.main.service.StatisticsService import StatisticsService
from src.main.model.JobOffer import JobOffer
from typing import List
import tkinter.font as tkfont
import webbrowser
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.number_of_offers = 0
        self.selected_button = None
        self.selected_offer = None
        self.database = DatabaseConfig()
        self.data = self.database.read_data()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.app = ctk.CTk()
        self.app.title("Job Scraper")
        self.app.geometry("1100x650")
        self.app.minsize(900, 600)

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=2)
        self.app.grid_rowconfigure(0, weight=1)

        self.font = tkfont.Font(family="Roboto", size=12)
        self.titles = [self.fix_text(offer.title) for offer in self.data]

    def on_refresh(self):
        log.info("Loading the configuration")
        config = ConfigLoader()
        websites = config.get_sites_config()

        log.info("Scraping the data")
        scraper = ScraperService(websites)
        offers: List[JobOffer] = scraper.scrape_all_sites()
        log.info(f"Found {len(offers)} offers")

        log.info("Saving the data")

        database = DatabaseConfig()
        database.create_table()
        self.data += database.insert_data(offers)
        self.titles = [self.fix_text(offer.title) for offer in self.data]

        self.fill_listbox()
        self.settings_status_label.configure(text=f"{self.number_of_offers} OFFERS FOUND")

    def on_visit(self):
        if self.selected_offer:
            webbrowser.open(self.selected_offer.url)

    def on_search(self):
        if self.search_entry.get().strip() != '':
            self.fill_listbox(lambda x: True if self.search_entry.get().lower() in x.lower() else False)
        else:
            self.fill_listbox()

    def on_clear(self):
        self.search_var.set('')
        self.fill_listbox()

    def on_offer_select(self, button, offer):
        if self.selected_button:
            self.selected_button.configure(fg_color="#3a3a3a")

        button.configure(fg_color="#1f6aa5")
        self.selected_button = button
        self.selected_offer = offer

        self.title_entry.configure(state="normal")
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, offer.title)
        self.title_entry.configure(state="disabled")

        if offer.location is not None:
            self.location_entry.configure(state="normal")
            self.location_entry.delete(0, "end")
            self.location_entry.insert(0, offer.location)
            self.location_entry.configure(state="disabled")

        if offer.salary is not None:
            self.salary_entry.configure(state="normal")
            self.salary_entry.delete(0, "end")
            self.salary_entry.insert(0, offer.salary)
            self.salary_entry.configure(state="disabled")

    def on_show_graph(self):
        s_service = StatisticsService()
        data = s_service.get_position_type_counts()

        x = list(data.keys())
        y = list(data.values())

        plt.figure(figsize=(10, 6))
        plt.bar(x, y, color='orange')

        plt.title('Number of offers in different areas', fontsize=16)
        plt.xlabel('Position', fontsize=12)
        plt.ylabel('Number of offers', fontsize=12)

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def main_frame_setup(self):
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def offer_frame_setup(self):
        self.offer_frame = ctk.CTkFrame(self.main_frame, border_width=2, corner_radius=0)
        self.offer_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10, rowspan=2)
        self.offer_frame.grid_columnconfigure(0, weight=1)
        self.offer_frame.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.offer_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.on_search())

        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search", font=("Roboto", 12))
        self.search_entry.grid(row=0, column=0, sticky="ew")

        clear_button = ctk.CTkButton(search_frame, text="Clear", width=50, command=self.on_clear, font=("Roboto", 12))
        clear_button.grid(row=0, column=1, padx=(6, 0))

        self.offer_list_box_setup()

    def offer_list_box_setup(self):
        self.listbox_frame = ctk.CTkScrollableFrame(self.offer_frame, border_width=2, corner_radius=0)
        self.listbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(2, 10))
        self.listbox_frame.grid_columnconfigure(0, weight=1)
        self.fill_listbox()

    def fix_text(self, text):
        if_changed = False
        while self.font.measure(text) > 476 and len(text) > 0:
            text = text[:-1]
            if_changed = True
        if if_changed:
            text = text[:-4] + ' ...'
        return text

    def fill_listbox(self, pred=lambda x: True):
        for child in self.listbox_frame.winfo_children():
            child.destroy()

        self.selected_button = None
        self.number_of_offers = len(self.data)
        is_first = True
        for element, title in zip(self.data, self.titles):
            if pred(element.title):
                button = ctk.CTkButton(
                    self.listbox_frame,
                    text=title,
                    anchor="w",
                    fg_color="#3a3a3a",
                    hover=True,
                    corner_radius=4,
                    font=("Roboto", 12)
                )
                button.configure(command=lambda b=button, o=element: self.on_offer_select(b, o))
                if is_first:
                    button.pack(fill="x", pady=8, padx=(8, 1))
                    is_first = False
                else:
                    button.pack(fill="x", pady=(0, 8), padx=(8, 1))

    def details_container_setup(self):
        self.details_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.details_container.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10, rowspan=2)
        self.details_container.grid_columnconfigure(0, weight=1)
        self.details_container.grid_rowconfigure(0, weight=7)
        self.details_container.grid_rowconfigure(1, weight=3)

    def details_setup(self):
        self.details_container_setup()

        right_frame = ctk.CTkFrame(self.details_container, border_width=2, corner_radius=0)
        right_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        details_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        details_frame.grid(row=0, column=0, sticky="new", padx=20, pady=(20, 0))
        details_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(details_frame, text="Title:", font=("Roboto", 12))
        title_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)

        self.title_entry = ctk.CTkEntry(details_frame, state="disabled", font=("Roboto", 12))
        self.title_entry.insert(0, "Title")
        self.title_entry.grid(row=0, column=1, sticky="ew", columnspan=2, pady=6)

        location_label = ctk.CTkLabel(details_frame, text="Location:", font=("Roboto", 12))
        location_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)

        self.location_entry = ctk.CTkEntry(details_frame, state="disabled", font=("Roboto", 12))
        self.location_entry.insert(0, "Location")
        self.location_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=6)

        salary_label = ctk.CTkLabel(details_frame, text="Salary:", font=("Roboto", 12))
        salary_label.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)

        self.salary_entry = ctk.CTkEntry(details_frame, state="disabled", font=("Roboto", 12))
        self.salary_entry.insert(0, "Salary")
        self.salary_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=6)

        visit_button = ctk.CTkButton(details_frame, text="Visit site", command=self.on_visit, font=("Roboto", 12))
        visit_button.grid(row=4, column=0, columnspan=3, pady=6, sticky="e")

    def settings_setup(self):
        settings_frame = ctk.CTkFrame(self.details_container, border_width=2, corner_radius=0)
        settings_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10, 0))
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_rowconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        center_frame.grid(row=0, column=0)

        self.settings_status_label = ctk.CTkLabel(center_frame, text=f"{self.number_of_offers} OFFERS FOUND", font=("Verdana", 28, "bold"))
        self.settings_status_label.pack()

        settings_refresh_button = ctk.CTkButton(center_frame, text="Refresh offers", command=self.on_refresh, font=("Roboto", 12))
        settings_refresh_button.pack(pady=10)

        view_graph_button = ctk.CTkButton(center_frame, text="Show graph", command=self.on_show_graph, font=("Roboto", 12))
        view_graph_button.pack()

    def run(self):
        self.main_frame_setup()
        self.offer_frame_setup()
        self.details_setup()
        self.settings_setup()
        self.app.mainloop()


if __name__ == "__main__":
    GUI().run()
