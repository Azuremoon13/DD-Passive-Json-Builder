import customtkinter as ctk
import json
import pyperclip
import requests
import ctypes
import os
import sys


class JSONBuilder:
	def __init__(self, root):
		self.root = root
		self.root.title("DD Passive Production JSON Builder")
		icon_path = self.get_resource_path("dino_depot_mascot_icon.ico")
		if os.path.exists(icon_path):
			self.root.iconbitmap(icon_path)
			if os.name == "nt":
				ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("DD_PP_Builder")
		self.root.geometry("1900x1200")
		
		self.data_entries = []
		self.temp_items = []
		self.temp_alts = []
		self.temp_consumes = []
		self.PPJson = {}
		
		self.main_frame = ctk.CTkFrame(self.root)
		self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
		
		self.dino_frame = ctk.CTkFrame(self.main_frame)
		self.dino_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
		self.dino_label = ctk.CTkLabel(self.dino_frame, text="Dino")
		self.dino_label.grid(row=0, column=0, columnspan=2, pady=5)
		
		self.item_frame = ctk.CTkFrame(self.main_frame)
		self.item_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
		self.item_label = ctk.CTkLabel(self.item_frame, text="Item")
		self.item_label.grid(row=0, column=0, columnspan=2, pady=5)

		self.alt_frame = ctk.CTkFrame(self.main_frame)
		self.alt_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")
		self.alt_label =ctk.CTkLabel(self.alt_frame, text="Alt Item")
		self.alt_label.grid(row=0, column=0, columnspan=2, pady=5)
		
		self.consume_frame = ctk.CTkFrame(self.main_frame)
		self.consume_frame.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
		self.consume_label = ctk.CTkLabel(self.consume_frame, text= "Consume Item")
		self.consume_label.grid(row=0, column=0, columnspan=2, pady=5)
		

		self.output_frame = ctk.CTkFrame(self.main_frame)
		self.output_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="sew")
		self.output_frame.grid_rowconfigure(0, weight=1)
		self.output_frame.grid_columnconfigure(0, weight=1)

		
		self.dino_dict = requests.get("https://raw.githubusercontent.com/Azuremoon13/DD-Passive-Json-Builder/refs/heads/main/Dino_List.json").json()
		self.resource_dict = requests.get("https://raw.githubusercontent.com/Azuremoon13/DD-Passive-Json-Builder/refs/heads/main/Resource_List.json").json()

		self.consume_modes = ["All items are produced", "One item at random", "One item round-robin"]
		self.combo_placeholder = {"dino": "Select a dino",
								  "item": "Select an item",
								  "alt": "All items are produced",
								  "consume": "All items are produced"}
		
		self.create_widgets()
	
	def get_resource_path(self, file_name):
		if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, file_name)
		else:
			return os.path.join(os.path.abspath(os.getcwd()), file_name)

	def create_widgets(self):
		def on_combobox_click(event):
			event.widget.delete(0, "end")

		labels = ["Dino Type:", "Chance To Produce"]
		
		self.text_boxes = []
		for i, label_text in enumerate(labels):
			label = ctk.CTkLabel(self.dino_frame, text=label_text)
			label.grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
			
			if "Dino Type:" in label_text:
				combo_box = ctk.CTkComboBox(self.dino_frame, width=300, values=[name for name in self.dino_dict.keys()])
				combo_box.name = "dino" if "Dino Type:" in label_text else "item"
				combo_box.set(self.combo_placeholder[combo_box.name])
				combo_box.grid(row=i+1, column=1, padx=5, pady=2)
				combo_box.bind("<Button-1>", on_combobox_click)
				self.text_boxes.append(combo_box)
			else:
				entry = ctk.CTkEntry(self.dino_frame, width=300, placeholder_text=0)
				entry.grid(row=i+1, column=1, padx=5, pady=2)
				self.text_boxes.append(entry)


		item_labels = ["Item:",
				"Interval (Seconds):",
				"Item Select Mode",
				"Quantity per Dino:",
				"Max per Cycle:",
				"Max in Terminal:",
				"Alt Select Mode:",
				"Alt Item Chance:",
				"Consume Select Mode:",
				"Consume Item Chance:"]
		
		for i, label_text in enumerate(item_labels):
			label = ctk.CTkLabel(self.item_frame, text=label_text)
			label.grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
			if label_text in ["Alt Select Mode:", "Consume Select Mode:", "Item Select Mode"]:
				combo_box = ctk.CTkComboBox(self.item_frame, width=300, values=self.consume_modes, state="readonly")
				combo_box.name = "alt" if "Alt Select Mode:" in label_text else "consume"
				combo_box.set(self.combo_placeholder[combo_box.name])
				combo_box.grid(row=i+1, column=1, padx=5, pady=2)
				combo_box.bind("<Button-1>", on_combobox_click)
				self.text_boxes.append(combo_box)

			elif "Item:" in label_text:
				combo_box = ctk.CTkComboBox(self.item_frame, width=300, values=[name for name in self.resource_dict.keys()])
				combo_box.name = "item"
				combo_box.set(self.combo_placeholder[combo_box.name])
				combo_box.grid(row=i+1, column=1, padx=5, pady=2)
				combo_box.bind("<Button-1>", on_combobox_click)
				self.text_boxes.append(combo_box)
				
			else:
				entry = ctk.CTkEntry(self.item_frame, width=300, placeholder_text=0)
				entry.grid(row=i+1, column=1, padx=5, pady=2)
				self.text_boxes.append(entry)
				
		alt_labels = ["Item:",
				"Quantity per Item:",
				"Max per Cycle:",
				"Max in Terminal:"]
		for i, label_text in enumerate(alt_labels):
			label = ctk.CTkLabel(self.alt_frame, text=label_text)
			label.grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
			if label_text in ["Item:"]:
				combo_box = ctk.CTkComboBox(self.alt_frame, width=300, values=[name for name in self.resource_dict.keys()])
				combo_box.name = "item"
				combo_box.set(self.combo_placeholder[combo_box.name])
				combo_box.grid(row=i+1, column=1, padx=5, pady=2)
				combo_box.bind("<Button-1>", on_combobox_click)
				self.text_boxes.append(combo_box)
			else:
				entry = ctk.CTkEntry(self.alt_frame, width=300, placeholder_text=0)
				entry.grid(row=i+1, column=1, padx=5, pady=2)
				self.text_boxes.append(entry)


		consume_labels = ["Item:",
					"Quantity per Item:",
					"Max per Cycle:"]
		for i, label_text in enumerate(consume_labels):
			label = ctk.CTkLabel(self.consume_frame, text=label_text)
			label.grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
			if label_text in ["Item:"]:
				combo_box = ctk.CTkComboBox(self.consume_frame, width=300, values=[name for name in self.resource_dict.keys()])
				combo_box.name = "item"
				combo_box.set(self.combo_placeholder[combo_box.name])
				combo_box.grid(row=i+1, column=1, padx=5, pady=2)
				combo_box.bind("<Button-1>", on_combobox_click)
				self.text_boxes.append(combo_box)
			else:
				entry = ctk.CTkEntry(self.consume_frame, width=300, placeholder_text=0)
				entry.grid(row=i+1, column=1, padx=5, pady=2)
				self.text_boxes.append(entry)

		self.text_box_json = ctk.CTkTextbox(self.output_frame, height=600, state="disabled")
		self.text_box_json.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
		
		self.add_entry_button = ctk.CTkButton(self.dino_frame, text="Add Passive entry", command=self.add_entry)
		self.add_entry_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=25)

		self.add_item_button = ctk.CTkButton(self.item_frame, text="Add item entry", command=self.add_item)
		self.add_item_button.grid(row=len(item_labels)+1, column=0, columnspan=2, pady=25)

		self.add_alt_button = ctk.CTkButton(self.alt_frame, text="Add alt item entry", command=self.add_alt)
		self.add_alt_button.grid(row=len(alt_labels)+1, column=0, columnspan=2, pady=25)

		self.add_consume_button = ctk.CTkButton(self.consume_frame, text="Add consumption entry", command=self.add_consume)
		self.add_consume_button.grid(row=len(consume_labels)+1, column=0, columnspan=2, pady=25)
		
		self.copy_button = ctk.CTkButton(self.output_frame, text="Copy JSON", command=self.copy_json)
		self.copy_button.grid(row=1, column=0, padx= 10, pady=10)

		self.remove_last_button = ctk.CTkButton(self.output_frame, text="Remove Last Entry", command=self.remove_last_entry)
		self.remove_last_button.grid(row=1, column=1, padx= 10, pady=10)

		self.clear_button = ctk.CTkButton(self.output_frame, text="Clear JSON", command=self.clear_json)
		self.clear_button.grid(row=1, column=2, padx= 10, pady=10)
		
		for box in self.text_boxes:
			if isinstance(box, ctk.CTkEntry):
				box.bind("<KeyRelease>", self.update_json)
			else:
				box.bind("<<ComboboxSelected>>", self.update_json)
	
	def get_entry_data(self):
		return {
			"dinoType": self.dino_dict.get(self.text_boxes[0].get(), self.text_boxes[0].get()),
			"chanceToProduce": float(self.text_boxes[1].get()) if self.text_boxes[1].get() else 0,
			"produces": [
				{
					"intervalSeconds": float(self.text_boxes[3].get()) if self.text_boxes[3].get() else 0,
					"itemSelectMode": self.consume_modes.index(self.text_boxes[4].get()) if self.text_boxes[4].get() else 0,
					"items": self.temp_items[:]
				}
			]
		}
	
	def add_entry(self):
		if self.text_boxes[0].get() not in ["Select a dino",""]:
			entry = self.get_entry_data()
			self.data_entries.append(entry)
			self.temp_items.clear()
			PPJson = {"version": 2, "production": self.data_entries}
			
			self.text_box_json.configure(state="normal")
			self.text_box_json.delete("1.0", "end")
			self.text_box_json.insert("1.0", json.dumps(PPJson, indent=4))
			self.text_box_json.configure(state="disabled")

			for box in self.text_boxes[0:]:
				if isinstance(box, ctk.CTkEntry):
					placeholder = box.cget("placeholder_text")
					box.delete(0, "end")
					box.configure(placeholder_text=placeholder)
				else:
					box.set(self.combo_placeholder[box.name])

	def add_item(self):
		if self.text_boxes[2].get() not in ["Select an item",""]:
			self.temp_items.append(
				{
					"bpPath": self.resource_dict.get(self.text_boxes[2].get(), self.text_boxes[2].get()),
					"maxQuantityPerCycle": int(self.text_boxes[6].get()) if self.text_boxes[6].get() else 0,
					"maxQuantityInTerminal": int(self.text_boxes[7].get()) if self.text_boxes[7].get() else 0,
					"quantityPerDino": int(self.text_boxes[5].get()) if self.text_boxes[5].get() else 0,
					"alternateSelectMode": self.consume_modes.index(self.text_boxes[8].get()) if self.text_boxes[8].get() else 0,
					"alternateItemsChance": float(self.text_boxes[9].get()) if self.text_boxes[9].get() else 0.0,
					"alternateItems": self.temp_alts[:],
					"consumesSelectMode": self.consume_modes.index(self.text_boxes[10].get()) if self.text_boxes[10].get() else 0,
					"consumesItemsChance": float(self.text_boxes[11].get()) if self.text_boxes[11].get() else 0.0,
					"consumesItems": self.temp_consumes[:]
				}
			)
			self.temp_alts.clear()
			self.temp_consumes.clear()
			for box in self.text_boxes[2:]:
				if isinstance(box, ctk.CTkEntry):
					placeholder = box.cget("placeholder_text")
					box.delete(0, "end")
					box.configure(placeholder_text=placeholder)
				else:
					box.set(self.combo_placeholder[box.name])
			self.update_json()				


	def add_alt(self):
		self.temp_alts.append(
			{
				"bpPath": self.resource_dict.get(self.text_boxes[12].get(), self.text_boxes[12].get()),
				"quantityPerItem": int(self.text_boxes[13].get()) if self.text_boxes[13].get() else 0,
				"maxQuantityPerCycle": int(self.text_boxes[14].get()) if self.text_boxes[14].get() else 0,
				"maxQuantityInTerminal": int(self.text_boxes[15].get()) if self.text_boxes[15].get() else 0
			}
		)
		for box in self.text_boxes[12:15]:
			if isinstance(box, ctk.CTkEntry):
				placeholder = box.cget("placeholder_text")
				box.delete(0, "end")
				box.configure(placeholder_text=placeholder)
			else:
				box.set(self.combo_placeholder[box.name])
		self.update_json()				

	def add_consume(self):
		self.temp_consumes.append(
			{
				"bpPath": self.resource_dict.get(self.text_boxes[16].get(), self.text_boxes[16].get()),
				"quantityPerItem": int(self.text_boxes[17].get()) if self.text_boxes[17].get() else 0,
				"maxQuantityPerCycle": int(self.text_boxes[18].get()) if self.text_boxes[18].get() else 0
			}
		)
		for box in self.text_boxes[16:]:
			if isinstance(box, ctk.CTkEntry):
				placeholder = box.cget("placeholder_text")
				box.delete(0, "end")
				box.configure(placeholder_text=placeholder)
			else:
				box.set(self.combo_placeholder[box.name])
		self.update_json()				


	def update_json(self, event=None):
		if not self.data_entries:
			self.PPJson = {"version": 2, "production": []}
		else:
			self.PPJson = {"version": 2, "production": self.data_entries}

		self.text_box_json.configure(state="normal")
		self.text_box_json.delete("1.0", "end")
		self.text_box_json.insert("1.0", json.dumps(self.PPJson, indent=4))
		self.text_box_json.configure(state="disabled")

	def copy_json(self):
		PPJson = {"version": 2, "production": self.data_entries}
		json_text = json.dumps(PPJson, indent=4)
		pyperclip.copy(json_text)
	
	def remove_last_entry(self):
		del self.data_entries[-1]
		self.update_json()
	
	def clear_json(self):
		self.data_entries.clear()
		self.update_json()

if __name__ == "__main__":
	ctk.set_appearance_mode("dark")
	root = ctk.CTk()
	app = JSONBuilder(root)
	root.mainloop()