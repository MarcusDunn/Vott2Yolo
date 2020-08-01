from dataclasses import dataclass
from typing import Dict, List, Tuple
from PIL import Image

names: List[str] = [
    "LCD_Screen",
    "Seal",
    "Continous_Amps",
    "Electric_Rating",
    "Service_Type",
    "Phase_Number",
    "Wire_Number",
    "Meter_Type",
    "KW_Max",
    "Multiplier",
    "Utility_Inventory_Number",
    "Serial_Number",
    "Dials",
    "Manufacture_Date",
    "Meter_Manufacture",
    "Kilovolt_Amperes",
    "Electric_Meter"
]


@dataclass
class YoloData:
    type_index: int
    x: float
    y: float
    width: float
    height: float

    def __init__(self, vott_data: "VottData", im_size: tuple):
        self.type_index = names.index(vott_data.label)
        self.x, self.y, self.width, self.height = self.parseVoTT(
            vott_data, im_size)

    def parseVoTT(self, vott_data: "VottData", im_size: Tuple[int, int]) -> Tuple[float, float, float, float]:
        im_width, im_height = im_size[0], im_size[1]
        x: float = (((vott_data.xMax - vott_data.xMin) / 2) +
                    vott_data.xMin) / im_width
        y: float = (((vott_data.yMax - vott_data.yMin)/2) +
                    vott_data.yMin / im_height)
        width: float = (vott_data.xMax - vott_data.xMin) / im_width
        height: float = (vott_data.yMax - vott_data.yMin) / im_height
        return x, y, width, height

    def __str__(self):
        return str(self.type_index) + " " + str(self.x) + " " + str(self.y) + " " + str(self.width) + " " + str(self.height)


@dataclass
class VottData:
    image: str
    xMin: float
    xMax: float
    yMin: float
    yMax: float
    label: str

    def __init__(self, data: list):
        self.image = data[0].replace("\"", "")
        self.xMin, self.xMax, self.yMin, self.yMax = map(
            lambda x: float(x), data[1:1])
        self.label = data[5].replace("\"", "").replace("\n", "")


def main():
    file: "File" = open("DefaultProject-export.csv", "r")
    data: Dict[str, List["VottData"]] = populate_data_from_csv(file)
    for k, v in data.items():
        label_file = k.replace(".jpg", ".txt")
        darkFile: File = open(label_file, "w")
        darkData: str = VoTT2Yolo(v)
        darkFile.write(darkData)


def VoTT2Yolo(vottData: List["VottData"]) -> str:
    ret: str = ""
    image: Image = Image.open(vottData[0].image)
    size: tuple = image.size
    for box in vottData:
        yolo: YoloData = YoloData(box, size)
        ret += str(yolo) + "\n"
    return ret


def populate_data_from_csv(file: "File") -> Dict[str, List["VottData"]]:
    data: Dict[str, List["VottData"]] = {}
    for line in file:
        try:
            vottData: "VottData" = parse_line(line)
            if vottData.image in data:
                data[vottData.image].append(vottData)
            else:
                data[vottData.image] = [vottData]
        except Exception:
            pass
    return data


def parse_line(line: str):
    line.replace(" ", "")
    return VottData(line.split(","))


if __name__ == "__main__":
    main()
