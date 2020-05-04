"""
TODO
"""
from typing import Optional, List
import numpy as _np
import pandas as _pd


class ObserverType(type):
    pass


class Observer(metaclass=ObserverType):
    def __init__(self, elements):
        self.elements = elements
        self.data = []
        self.headers = []

    def __call__(self, element: Optional[List[str]], b1, b2):
        if self.elements is None:
            return True
        if element.LABEL1 not in self.elements:
            return False
        else:
            return True

    def to_df(self) -> _pd.DataFrame:
        return _pd.DataFrame(self.data, columns=self.headers)


class BeamObserver(Observer):
    def __init__(self, elements: Optional[List[str]] = None, with_input_beams: bool = False):
        super().__init__(elements)
        self._with_input_beams = with_input_beams
        self.headers = ('LABEL1', 'BEAM_IN', 'BEAM_OUT')

    def __call__(self, element, b1, b2):
        if super().__call__(element, b1, b2):
            self.data.append((element.LABEL1, _np.copy(b1) if self._with_input_beams else None, _np.copy(b2)))


class SuperObserver(Observer):
    def __init__(self, elements: Optional[List[str]] = None):
        super().__init__(elements)
        self.headers = ('LABEL1',
                        )

    def __call__(self, element, b1, b2):
        if super().__call__(element, b1, b2):
            self.data.append((element.LABEL1, ))


class MeanObserver(Observer):
    def __init__(self, elements: Optional[List[str]] = None):
        super().__init__(elements)
        self.headers = ('LABEL1',
                        'BEAM_IN_X',
                        'BEAM_OUT_X',
                        'BEAM_IN_Y',
                        'BEAM_OUT_Y',
                        'BEAM_IN_XP',
                        'BEAM_OUT_XP',
                        'BEAM_IN_YP',
                        'BEAM_OUT_YP',
                        'BEAM_IN_DPP',
                        'BEAM_OUT_DPP',
                        )

    def __call__(self, element, b1, b2):
        if super().__call__(element, b1, b2):
            self.data.append((element.LABEL1,
                              b1[:, 0].mean(),
                              b2[:, 0].mean(),
                              b1[:, 2].mean(),
                              b2[:, 2].mean(),
                              b1[:, 1].mean(),
                              b2[:, 1].mean(),
                              b1[:, 3].mean(),
                              b2[:, 3].mean(),
                              b1[:, 4].mean(),
                              b2[:, 4].mean(),
                              ))


class SigmaObserver(Observer):
    def __init__(self, elements: Optional[List[str]] = None):
        super().__init__(elements)
        self.headers = ('LABEL1',
                        'BEAM_IN_X',
                        'BEAM_OUT_X',
                        'BEAM_IN_Y',
                        'BEAM_OUT_Y',
                        'BEAM_IN_XP',
                        'BEAM_OUT_XP',
                        'BEAM_IN_YP',
                        'BEAM_OUT_YP',
                        'BEAM_IN_DPP',
                        'BEAM_OUT_DPP',
                        )

    def __call__(self, element, b1, b2):
        if super().__call__(element, b1, b2):
            self.data.append((element.LABEL1,
                              b1[:, 0].std(),
                              b2[:, 0].std(),
                              b1[:, 2].std(),
                              b2[:, 2].std(),
                              b1[:, 1].std(),
                              b2[:, 1].std(),
                              b1[:, 3].std(),
                              b2[:, 3].std(),
                              b1[:, 4].std(),
                              b2[:, 4].std(),
                              ))


class LossesObserver(Observer):
    def __init__(self, elements: Optional[List[str]] = None):
        super().__init__(elements)
        self.headers = ('LABEL1',
                        'PARTICLES_IN',
                        'PARTICLES_OUT',
                        'TRANSMISSION',
                        'LOSSES',
                        )

    def __call__(self, element, b1, b2):
        if super().__call__(element, b1, b2):
            self.data.append((element.LABEL1,
                              b1.shape[0],
                              b2.shape[0],
                              100 * (b2.shape[0] / b1.shape[0]),
                              100 * (1 - b2.shape[0] / b1.shape[0]),
                              ))

    def compute_global_transmission(self, global_transmission: float = 1.0):
        for elem in self.data:
            global_transmission *= elem[3]/100
        return global_transmission*100

    def compute_global_losses(self):
        return 100-self.compute_global_transmission()

    #def adjust_for_efficiency(self, efficiency: float = 1.0):
        # do something with self.data
        # self.data['LOSSES'] /= efficiency
        # self.data['TRANSMISSION'] *= effiency
     #   ...


class SymmetryObserver(Observer):
    def __init__(self):
        super().__init__()

        self.headers = ('LABEL1',
                        'SYM_IN',
                        'SYM_OUT',
                        )

    def __call__(self, element, b1, b2):
        self.data.append((element.LABEL1,
                          abs(b1[:, 0].std() - b1[:, 2].std()) / (b1[:, 0].std() + b1[:, 2].std()),
                          abs(b2[:, 0].std() - b2[:, 2].std()) / (b2[:, 0].std() + b2[:, 2].std()),
                          ))


class IbaBpmObserver(Observer):
    ...
