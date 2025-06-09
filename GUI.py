import customtkinter as ctk
from DatabaseConfig import DatabaseConfig
from logger_config import log
from ConfigLoader import ConfigLoader
from ScraperService import ScraperService
from JobOffer import JobOffer
from typing import List
import webbrowser


class JobOffersGUI:
    def __init__(self):
        self.selected_button = None
        self.selected_offer = None
        self.database = DatabaseConfig()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Job Offers")
        self.app.geometry("1100x650")
        self.app.minsize(900, 600)

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=2)
        self.app.grid_rowconfigure(0, weight=1)

    def on_scrape(self):
        log.info("Loading the configuration")
        config = ConfigLoader()
        websites = config.get_sites_config()

        log.info("Scraping the data")
        scraper = ScraperService(websites)
        offers: List[JobOffer] = scraper.scrape_all_sites()
        log.info(f"Found {len(offers)} offers")

        log.info("Saving the data")

        database = DatabaseConfig()
        database.create_database()
        database.create_table()
        database.insert_data(offers)

    def on_visit(self):
        if self.selected_offer:
            webbrowser.open(self.selected_offer['url'])

    def on_search(self):
        if self.search_entry.get().strip() != '':
            self.fill_listbox(lambda x: True if self.search_entry.get().lower() in x.lower() else False)
        else:
            self.fill_listbox()

    def on_offer_select(self, button, offer):
        if self.selected_button:
            self.selected_button.configure(fg_color="#3a3a3a")

        button.configure(fg_color="#1f6aa5")
        self.selected_button = button
        self.selected_offer = offer

        self.title_entry.configure(state="normal")
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, offer['title'])
        self.title_entry.configure(state="disabled")

        if offer['location'] is not None:
            self.location_entry.configure(state="normal")
            self.location_entry.delete(0, "end")
            self.location_entry.insert(0, offer['location'])
            self.location_entry.configure(state="disabled")

        if offer['salary'] is not None:
            self.salary_entry.configure(state="normal")
            self.salary_entry.delete(0, "end")
            self.salary_entry.insert(0, offer['salary'])
            self.salary_entry.configure(state="disabled")

    def on_update(self):
        try:
            number_of_days = int(self.days_entry.get())
        except ValueError:
            pass

    def offer_frame(self):
        self.left_frame = ctk.CTkFrame(self.app, border_width=2, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10, rowspan=2)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search")
        self.search_entry.grid(row=0, column=0, sticky="ew")

        search_btn = ctk.CTkButton(search_frame, text="🔍", width=50, command=self.on_search)
        search_btn.grid(row=0, column=1, padx=(6, 0))

        self.offer_list_box()

    def offer_list_box(self):
        self.listbox_frame = ctk.CTkScrollableFrame(self.left_frame, border_width=2, corner_radius=0)
        self.listbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.listbox_frame.grid_columnconfigure(0, weight=1)
        self.fill_listbox()

    def fill_listbox(self, pred=lambda x: True):
        for child in self.listbox_frame.winfo_children():
            child.destroy()

        self.selected_button = None
        for element in self.database.read_data():
            if pred(element['title']):
                btn = ctk.CTkButton(
                    self.listbox_frame,
                    text=element['title'],
                    anchor="w",
                    fg_color="#3a3a3a",
                    hover=True,
                    corner_radius=4,
                )
                btn.configure(command=lambda b=btn, off=element: self.on_offer_select(b, off))
                btn.pack(fill="x", pady=4, padx=2)

    def right_container(self):
        self.right_container = ctk.CTkFrame(self.app, fg_color="transparent")
        self.right_container.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10, rowspan=2)
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(0, weight=7)
        self.right_container.grid_rowconfigure(1, weight=3)

    def offer_details(self):
        right_frame = ctk.CTkFrame(self.right_container, border_width=2, corner_radius=0)
        right_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        details_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        details_frame.grid(row=0, column=0, sticky="new", padx=20, pady=(20, 0))
        details_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(details_frame, text="Title:")
        title_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)

        self.title_entry = ctk.CTkEntry(details_frame, state="disabled")
        self.title_entry.insert(0, "Title")
        self.title_entry.grid(row=0, column=1, sticky="ew", columnspan=2, pady=6)

        location_label = ctk.CTkLabel(details_frame, text="Location:")
        location_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)

        self.location_entry = ctk.CTkEntry(details_frame, state="disabled")
        self.location_entry.insert(0, "Location")
        self.location_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=6)

        salary_label = ctk.CTkLabel(details_frame, text="Salary:")
        salary_label.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)

        self.salary_entry = ctk.CTkEntry(details_frame, state="disabled")
        self.salary_entry.insert(0, "Salary")
        self.salary_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=6)

        visit_btn = ctk.CTkButton(details_frame, text="Visit site", command=self.on_visit)
        visit_btn.grid(row=4, column=0, columnspan=3, pady=6, sticky="e")

    def settings(self):
        bottom_frame = ctk.CTkFrame(self.right_container, border_width=2, corner_radius=0)
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(10, 0))
        bottom_frame.grid_columnconfigure(0, weight=7)
        bottom_frame.grid_columnconfigure(1, weight=3)
        bottom_frame.grid_rowconfigure(0, weight=1)

        self.left_subframe = ctk.CTkFrame(bottom_frame, corner_radius=0)
        self.left_subframe.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.left_subframe.grid_columnconfigure(0, weight=1)

        mail_label_row = ctk.CTkFrame(self.left_subframe, fg_color="transparent")
        mail_label_row.grid(row=0, column=0, sticky="ew", pady=(10, 5))

        lbl_days = ctk.CTkLabel(mail_label_row, text="days")
        lbl_days.pack(side="right", padx=(0, 10))

        self.days_entry = ctk.CTkEntry(mail_label_row, width=80)
        self.days_entry.pack(side="right", padx=(6, 6))
        self.days_entry.insert(0, "3")

        lbl_text = ctk.CTkLabel(mail_label_row, text="The offers are updated once every")
        lbl_text.pack(side="right")

        update_btn = ctk.CTkButton(self.left_subframe, text="Update", command=self.on_update)
        update_btn.grid(row=1, column=0, pady=10)

        self.right_subframe = ctk.CTkFrame(bottom_frame, corner_radius=0)
        self.right_subframe.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.right_subframe.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.right_subframe, text="... offers found", justify="center")
        self.status_label.grid(row=0, column=0, pady=(10, 10), padx=10)

        search_btn = ctk.CTkButton(self.right_subframe, text="Search offers", command=self.on_scrape)
        search_btn.grid(row=1, column=0, pady=(0, 10))

    def run(self):
        self.offer_frame()
        self.offer_list_box()
        self.right_container()
        self.offer_details()
        self.settings()
        self.app.mainloop()


if __name__ == "__main__":
    JobOffersGUI().run()
