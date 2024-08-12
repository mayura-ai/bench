from bench.parsers.physics import BaseData as PhysData
from bench.parsers.mathematics import BaseData as MathData
from bench.parsers.chemistry import BaseData as ChemData


def main():
    # (TODO): CLI interface
    data = MathData()
    data.add_data_items(
        data.parse(
            url="https://byjus.com/jee/jee-main-2022-question-paper-maths-july-25-shift-1/"
        )
    )
    data.save("math.json")

    data = PhysData()
    data.add_data_items(
        data.parse(
            url="https://byjus.com/jee/jee-main-2022-question-paper-physics-july-25-shift-1/"
        )
    )
    data.save("phys.json")

    data = ChemData()
    data.add_data_items(
        data.parse(
            url="https://byjus.com/jee/jee-main-2022-question-paper-chemistry-july-25-shift-1/"
        )
    )
    data.save("chem.json")


if __name__ == "__main__":
    main()
