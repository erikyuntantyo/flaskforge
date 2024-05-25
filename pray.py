class LordPrayer:
    def __init__(self):
        self.pray: str = """
        oLIW'H kIZBVI YB qVHFH xSIRHG

        lFI uZGSVI RM SVZEVM,
        SZOOLDVW YV BLFI MZNV,
        BLFI PRMTWLN XLNV,
        BLFI DROO YV WLMV,
        LM VZIGS ZH RM SVZEVM.

        tREV FH GLWZB LFI WZROB YIVZW.
        uLITREV FH LFI HRMH
        ZH DV ULITREV GSLHV DSL HRM ZTZRMHG FH.

        oVZW FH MLG RMGL GVNKGZGRLM
        YFG WVOREVI FH UILN VERO.
        uLI GSV PRMTWLN, GSV KLDVI,
        ZMW GSV TOLIB ZIV BLFIH
        MLD ZMW ULI VEVI.

        zNVM."""

    def __in_the_name_of_jesus__(self) -> str:
        a: list = [(i + j) for i in (65, 97) for j in range(26)]
        b: list = [(i + j) for i in (97, 65) for j in range(25, -1, -1)]
        chars: dict = dict(list(map(lambda a, b: (chr(a), chr(b)), a, b)))
        self.pray = "".join(list(map(lambda c: chars.get(c, c), [c for c in self.pray])))

        return self.pray

    def __str__(self) -> str:
        return self.__in_the_name_of_jesus__()


print(LordPrayer())
