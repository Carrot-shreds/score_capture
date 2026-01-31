from functools import singledispatch
from typing import Any, Callable

from loguru import logger as log
from pydantic import ValidationError
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QWidget,
)

from src.Model.Data.type import NonEmptyStr, OnValueChangeModel

data_binding_map: dict[
    QWidget | OnValueChangeModel,
    dict[QWidget | OnValueChangeModel, dict[str, Callable[[Any], None]]],
] = {}


def set_model_field(model: OnValueChangeModel, field: NonEmptyStr, value: Any):
    try:
        setattr(model, field, value)
    except ValidationError as e:
        log.debug(e)


def add_binding_map(
    a: QWidget | OnValueChangeModel,
    b: QWidget | OnValueChangeModel,
    prop: str,
    func: Callable,
) -> None:
    pass
    # if not data_binding_map.get(a):
    #     data_binding_map[a] = {}
    # if not data_binding_map[a].get(b):
    #     data_binding_map[a][b] = {}
    #     data_binding_map[a][b][prop] = func


@singledispatch
def bind_data(
    widget: QTextEdit,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setText(str(v)))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        widget.textChanged.connect(w2d := lambda v: set_model_field(data, prop, v))
        add_binding_map(widget, data, prop, w2d)


@bind_data.register(QLabel)
def _(
    widget: QLabel,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setText(str(v)))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)


@bind_data.register(QComboBox)
def _(
    widget: QComboBox,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
    use_index=False,
):
    if use_index:
        data.add_observer_handler(prop, d2w := lambda v: widget.setCurrentIndex(v))
    else:
        data.add_observer_handler(prop, d2w := lambda v: widget.setCurrentText(v))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        if use_index:
            widget.currentIndexChanged.connect(
                w2d := lambda v: set_model_field(data, prop, v)
            )
        else:
            widget.currentTextChanged.connect(
                w2d := lambda v: set_model_field(data, prop, v)
            )
        add_binding_map(widget, data, prop, w2d)


@bind_data.register(QSpinBox)
def _(
    widget: QSpinBox,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setValue(v))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        widget.valueChanged.connect(w2d := lambda v: set_model_field(data, prop, v))
        add_binding_map(widget, data, prop, w2d)


@bind_data.register(QDoubleSpinBox)
def _(
    widget: QDoubleSpinBox,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setValue(v))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        widget.valueChanged.connect(w2d := lambda v: set_model_field(data, prop, v))
        add_binding_map(widget, data, prop, w2d)


@bind_data.register(QCheckBox)
def _(
    widget: QCheckBox,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setChecked(v))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        widget.toggled.connect(w2d := lambda v: set_model_field(data, prop, v))
        add_binding_map(widget, data, prop, w2d)


@bind_data.register(QRadioButton)
def _(
    widget: QRadioButton,
    data: OnValueChangeModel,
    prop: NonEmptyStr,
    one_way: bool = False,
):
    data.add_observer_handler(prop, d2w := lambda v: widget.setChecked(v))
    d2w(getattr(data, prop))  # update default data vaule
    add_binding_map(data, widget, prop, d2w)
    if not one_way:
        widget.toggled.connect(w2d := lambda v: set_model_field(data, prop, v))
        add_binding_map(widget, data, prop, w2d)
