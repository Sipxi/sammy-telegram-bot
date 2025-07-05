from bs4 import BeautifulSoup
import json
import os


class VUTHTMLParser:
    def __init__(self, directory="data"):
        self.soup = None
        self.main_directory = directory
    def parse(self):
        """Main method to parse all exam entries"""
        entries = []
        for block in self.soup.find_all("div", class_="m_ppzc"):
            try:
                entry = {
                    "subject": self._parse_subject(block),
                    "type": self._parse_type(block),
                    "date": self._parse_date(block),
                    "result": self._parse_result(block),
                    "lecturer": self._parse_lecturer(block),
                    "room": self._parse_room(block),
                    "num_of_registered_people": self._parse_registered_count(block),
                    "is_registered": self._parse_registration_status(block),
                }
                entries.append(entry)
            except Exception as e:
                print(f"⚠️ Error parsing block: {e}")
        print("✅ Successfully parsed all entries.")
        return entries

    def _parse_subject(self, block):
        subject_span = block.select_one(".m_nadpis .hlavni")
        return subject_span.get_text(strip=True) if subject_span else None

    def _parse_type(self, block):
        div = block.select_one(".m_nadpis")
        if not div:
            return None

        subject_span = div.select_one("span.hlavni")
        full_text = div.get_text(strip=True)

        if subject_span:
            subject_text = subject_span.get_text(strip=True)
            exam_type = full_text.replace(subject_text, "").strip(" —().").strip("?")
            return exam_type or None

        return None

    def _parse_date(self, block):
        date_span = block.select_one(".m_podnadpis .hlavni")
        return date_span.get_text(strip=True) if date_span else None

    def _parse_registration_status(self, block):
        links = block.select(".m_podnadpis a")
        registration_link = links[1] if len(links) > 1 else None
        raw = registration_link.get_text(strip=True) if registration_link else None
        return {
            "status": bool(raw),
            "raw_data": raw
        }

    def _parse_result(self, block):
        result_b = block.select_one(".m_tinfo b")
        if not result_b:
            return None
        result_text = result_b.get_text(strip=True).lower()
        if "splněno" in result_text:
            return "splněno"
        elif "b." in result_text:
            return result_b.get_text(strip=True)
        elif "započteno" in result_text:
            return "započteno"
        return result_b.get_text(strip=True)

    def _parse_lecturer(self, block):
        lecturer_link = block.select_one(".m_tinfo a")
        return lecturer_link.get_text(strip=True) if lecturer_link else None

    def _parse_room(self, block):
        room_spans = block.select(".m_tinfo .bs_ttip")
        if not room_spans:
            return None
        return ", ".join(span.get("title", span.get_text(strip=True)) for span in room_spans)

    def _parse_registered_count(self, block):
        info_div = block.select_one(".m_tinfo")
        if not info_div:
            return None
        text = info_div.get_text(strip=True)
        if "přihlášení:" in text:
            parts = text.split("přihlášení:")[1].split(")")[0].strip()
            return f"{parts})"
        return None

    def read_file(self, input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            html_data = f.read()
            self.soup = BeautifulSoup(html_data, 'html.parser')
        
    def run(self, input_file="page.html", output_file="parsed_data.json"):
        """Parse HTML and save JSON result. Supports smart input/output paths."""
        self.read_file(input_file)
        parsed_data = self.parse()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        #  Normalize input path (relative to script)
        input_file = os.path.normpath(input_file)
        if not os.path.isabs(input_file):
            input_file = os.path.join(base_dir, input_file)

        #  Normalize output path
        output_file = os.path.normpath(output_file)
        if os.path.dirname(output_file):  # e.g. "somefolder/output.json"
            full_output_path = os.path.join(base_dir, output_file)
        else:
            full_output_path = os.path.join(base_dir, self.main_directory, output_file)

        #  Ensure target folder exists
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        print(f"Saving parsed data to {full_output_path}...")

        with open(full_output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Parsed {len(parsed_data)} entries and saved to '{output_file}'.")