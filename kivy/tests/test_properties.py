'''
Test properties attached to a widget
'''

import unittest
import pytest
from kivy.event import EventDispatcher
from functools import partial


class _TestProperty(EventDispatcher):
    pass


wid = _TestProperty()


@pytest.fixture(autouse=True)
def set_clock(kivy_clock):
    pass


@pytest.fixture()
def self():
    return unittest.TestCase()


@pytest.mark.parametrize('set_name', [True, False])
def test_base(self, set_name):
    from kivy.properties import Property

    a = Property(-1)
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), -1)
    a.set(wid, 0)
    self.assertEqual(a.get(wid), 0)
    a.set(wid, 1)
    self.assertEqual(a.get(wid), 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_observer(self, set_name):
    from kivy.properties import Property

    a = Property(-1)
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), -1)
    global observe_called
    observe_called = 0

    def observe(obj, value):
        global observe_called
        observe_called = 1
    a.bind(wid, observe)

    a.set(wid, 0)
    self.assertEqual(a.get(wid), 0)
    self.assertEqual(observe_called, 1)
    observe_called = 0
    a.set(wid, 0)
    self.assertEqual(a.get(wid), 0)
    self.assertEqual(observe_called, 0)
    a.set(wid, 1)
    self.assertEqual(a.get(wid), 1)
    self.assertEqual(observe_called, 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_objectcheck(self, set_name):
    from kivy.properties import ObjectProperty

    a = ObjectProperty(False)
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), False)
    a.set(wid, True)
    self.assertEqual(a.get(wid), True)


@pytest.mark.parametrize('set_name', [True, False])
def test_stringcheck(self, set_name):
    from kivy.properties import StringProperty

    a = StringProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), '')
    a.set(wid, 'hello')
    self.assertEqual(a.get(wid), 'hello')

    try:
        a.set(wid, 88)  # number shouldn't be accepted
        self.fail('string accept number, fail.')
    except ValueError:
        pass


@pytest.mark.parametrize('set_name', [True, False])
def test_numericcheck(self, set_name):
    from kivy.properties import NumericProperty

    a = NumericProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), 0)
    a.set(wid, 99)
    self.assertEqual(a.get(wid), 99)

    # try:
    #    a.set(wid, '')  # string shouldn't be accepted
    #    self.fail('number accept string, fail.')
    # except ValueError:
    #    pass


@pytest.mark.parametrize('set_name', [True, False])
def test_listcheck(self, set_name):
    from kivy.properties import ListProperty

    a = ListProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), [])
    a.set(wid, [1, 2, 3])
    self.assertEqual(a.get(wid), [1, 2, 3])


@pytest.mark.parametrize('set_name', [True, False])
def test_dictcheck(self, set_name):
    from kivy.properties import DictProperty

    a = DictProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), {})
    a.set(wid, {'foo': 'bar'})
    self.assertEqual(a.get(wid), {'foo': 'bar'})


@pytest.mark.parametrize('set_name', [True, False])
def test_propertynone(self, set_name):
    from kivy.properties import NumericProperty

    a = NumericProperty(0, allownone=True)
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), 0)
    try:
        a.set(wid, None)
        self.assertEqual(a.get(wid), None)
    except ValueError:
        pass
    a.set(wid, 1)
    self.assertEqual(a.get(wid), 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_reference(self, set_name):
    from kivy.properties import NumericProperty, ReferenceListProperty

    x = NumericProperty(0)
    if set_name:
        x.set_name(wid, 'x')
        x.link_eagerly(wid)
    else:
        x.link(wid, 'x')
        x.link_deps(wid, 'x')
    y = NumericProperty(0)
    if set_name:
        y.set_name(wid, 'y')
        y.link_eagerly(wid)
    else:
        y.link(wid, 'y')
        y.link_deps(wid, 'y')
    pos = ReferenceListProperty(x, y)
    if set_name:
        pos.set_name(wid, 'pos')
        pos.link_eagerly(wid)
    else:
        pos.link(wid, 'pos')
        pos.link_deps(wid, 'pos')

    self.assertEqual(x.get(wid), 0)
    self.assertEqual(y.get(wid), 0)
    self.assertEqual(pos.get(wid), [0, 0])

    x.set(wid, 50)
    self.assertEqual(pos.get(wid), [50, 0])

    y.set(wid, 50)
    self.assertEqual(pos.get(wid), [50, 50])

    pos.set(wid, [0, 0])
    self.assertEqual(pos.get(wid), [0, 0])
    self.assertEqual(x.get(wid), 0)
    self.assertEqual(y.get(wid), 0)

    # test observer
    global observe_called
    observe_called = 0

    def observe(obj, value):
        global observe_called
        observe_called = 1
    pos.bind(wid, observe)

    self.assertEqual(observe_called, 0)
    x.set(wid, 99)
    self.assertEqual(observe_called, 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_reference_child_update(self, set_name):
    from kivy.properties import NumericProperty, ReferenceListProperty

    x = NumericProperty(0)
    if set_name:
        x.set_name(wid, 'x')
        x.link_eagerly(wid)
    else:
        x.link(wid, 'x')
        x.link_deps(wid, 'x')
    y = NumericProperty(0)
    if set_name:
        y.set_name(wid, 'y')
        y.link_eagerly(wid)
    else:
        y.link(wid, 'y')
        y.link_deps(wid, 'y')
    pos = ReferenceListProperty(x, y)
    if set_name:
        pos.set_name(wid, 'pos')
        pos.link_eagerly(wid)
    else:
        pos.link(wid, 'pos')
        pos.link_deps(wid, 'pos')

    pos.get(wid)[0] = 10
    self.assertEqual(pos.get(wid), [10, 0])

    pos.get(wid)[:] = (20, 30)
    self.assertEqual(pos.get(wid), [20, 30])


@pytest.mark.parametrize('set_name', [True, False])
def test_dict(self, set_name):
    from kivy.properties import DictProperty

    x = DictProperty()
    if set_name:
        x.set_name(wid, 'x')
        x.link_eagerly(wid)
    else:
        x.link(wid, 'x')
        x.link_deps(wid, 'x')

    # test observer
    global observe_called
    observe_called = 0

    def observe(obj, value):
        global observe_called
        observe_called = 1

    x.bind(wid, observe)

    observe_called = 0
    x.get(wid)['toto'] = 1
    self.assertEqual(observe_called, 1)

    observe_called = 0
    x.get(wid)['toto'] = 2
    self.assertEqual(observe_called, 1)

    observe_called = 0
    x.get(wid)['youupi'] = 2
    self.assertEqual(observe_called, 1)

    observe_called = 0
    del x.get(wid)['toto']
    self.assertEqual(observe_called, 1)

    observe_called = 0
    x.get(wid).update({'bleh': 5})
    self.assertEqual(observe_called, 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_bounded_numeric_property(self, set_name):
    from kivy.properties import BoundedNumericProperty

    bnp = BoundedNumericProperty(0.0, min=0.0, max=3.5)

    if set_name:
        bnp.set_name(wid, 'bnp')
        bnp.link_eagerly(wid)
    else:
        bnp.link(wid, 'bnp')
        bnp.link_deps(wid, 'bnp')

    bnp.set(wid, 1)
    bnp.set(wid, 0.0)
    bnp.set(wid, 3.1)
    bnp.set(wid, 3.5)
    self.assertRaises(ValueError, partial(bnp.set, wid, 3.6))
    self.assertRaises(ValueError, partial(bnp.set, wid, -3))


@pytest.mark.parametrize('set_name', [True, False])
def test_bounded_numeric_property_error_value(self, set_name):
    from kivy.properties import BoundedNumericProperty

    bnp = BoundedNumericProperty(0, min=-5, max=5, errorvalue=1)
    if set_name:
        bnp.set_name(wid, 'bnp')
        bnp.link_eagerly(wid)
    else:
        bnp.link(wid, 'bnp')
        bnp.link_deps(wid, 'bnp')

    bnp.set(wid, 1)
    self.assertEqual(bnp.get(wid), 1)

    bnp.set(wid, 5)
    self.assertEqual(bnp.get(wid), 5)

    bnp.set(wid, 6)
    self.assertEqual(bnp.get(wid), 1)

    bnp.set(wid, -5)
    self.assertEqual(bnp.get(wid), -5)

    bnp.set(wid, -6)
    self.assertEqual(bnp.get(wid), 1)


@pytest.mark.parametrize('set_name', [True, False])
def test_bounded_numeric_property_error_handler(self, set_name):
    from kivy.properties import BoundedNumericProperty

    bnp = BoundedNumericProperty(
        0, min=-5, max=5,
        errorhandler=lambda x: 5 if x > 5 else -5)

    if set_name:
        bnp.set_name(wid, 'bnp')
        bnp.link_eagerly(wid)
    else:
        bnp.link(wid, 'bnp')
        bnp.link_deps(wid, 'bnp')

    bnp.set(wid, 1)
    self.assertEqual(bnp.get(wid), 1)

    bnp.set(wid, 5)
    self.assertEqual(bnp.get(wid), 5)

    bnp.set(wid, 10)
    self.assertEqual(bnp.get(wid), 5)

    bnp.set(wid, -5)
    self.assertEqual(bnp.get(wid), -5)

    bnp.set(wid, -10)
    self.assertEqual(bnp.get(wid), -5)


@pytest.mark.parametrize('set_name', [True, False])
def test_numeric_string_with_units_check(self, set_name):
    from kivy.properties import NumericProperty
    from kivy.metrics import Metrics

    a = NumericProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), 0)

    a.set(wid, '55dp')
    density = Metrics.density
    self.assertAlmostEqual(a.get(wid), 55 * density, delta=1E-2)
    self.assertEqual(a.get_format(wid), 'dp')

    a.set(wid, u'55dp')
    self.assertAlmostEqual(a.get(wid), 55 * density, delta=1E-2)
    self.assertEqual(a.get_format(wid), 'dp')

    a.set(wid, '99in')
    self.assertAlmostEqual(a.get(wid), 9504.0 * density, delta=1E-2)
    self.assertEqual(a.get_format(wid), 'in')

    a.set(wid, u'99in')
    self.assertAlmostEqual(a.get(wid), 9504.0 * density, delta=1E-2)
    self.assertEqual(a.get_format(wid), 'in')


@pytest.mark.parametrize('set_name', [True, False])
def test_numeric_string_without_units(self, set_name):
    from kivy.properties import NumericProperty

    a = NumericProperty()
    if set_name:
        a.set_name(wid, 'a')
        a.link_eagerly(wid)
    else:
        a.link(wid, 'a')
        a.link_deps(wid, 'a')
    self.assertEqual(a.get(wid), 0)

    a.set(wid, '2')
    self.assertEqual(a.get(wid), 2)


def test_property_rebind(self):
    from kivy.uix.label import Label
    from kivy.uix.togglebutton import ToggleButton
    from kivy.lang import Builder
    from kivy.properties import ObjectProperty, DictProperty, AliasProperty
    from kivy.clock import Clock

    class ObjWidget(Label):
        button = ObjectProperty(None, rebind=True, allownone=True)

    class ObjWidgetRebindFalse(Label):
        button = ObjectProperty(None, rebind=False, allownone=True)

    class DictWidget(Label):
        button = DictProperty({'button': None}, rebind=True,
                              allownone=True)

    class DictWidgetFalse(Label):
        button = DictProperty({'button': None}, rebind=False)

    class AliasWidget(Label):
        _button = None

        def setter(self, value):
            self._button = value
            return True

        def getter(self):
            return self._button
        button = AliasProperty(getter, setter, rebind=True)

    Builder.load_string('''
<ObjWidget>:
    text: self.button.state if self.button is not None else 'Unset'

<ObjWidgetRebindFalse>:
    text: self.button.state if self.button is not None else 'Unset'

<AliasWidget>:
    text: self.button.state if self.button is not None else 'Unset'

<DictWidget>:
    text: self.button.button.state if self.button.button is not None\
 else 'Unset'

<DictWidgetFalse>:
    text: self.button.button.state if self.button.button is not None\
 else 'Unset'
''')

    obj = ObjWidget()
    obj_false = ObjWidgetRebindFalse()
    dict_rebind = DictWidget()
    dict_false = DictWidgetFalse()
    alias_rebind = AliasWidget()
    button = ToggleButton()
    Clock.tick()
    self.assertEqual(obj.text, 'Unset')
    self.assertEqual(obj_false.text, 'Unset')
    self.assertEqual(dict_rebind.text, 'Unset')
    self.assertEqual(dict_false.text, 'Unset')
    self.assertEqual(alias_rebind.text, 'Unset')

    obj.button = button
    obj_false.button = button
    dict_rebind.button.button = button
    dict_false.button.button = button
    alias_rebind.button = button
    Clock.tick()
    self.assertEqual(obj.text, 'normal')
    self.assertEqual(obj_false.text, 'normal')
    self.assertEqual(dict_rebind.text, 'normal')
    self.assertEqual(dict_false.text, 'Unset')
    self.assertEqual(alias_rebind.text, 'normal')

    button.state = 'down'
    Clock.tick()
    self.assertEqual(obj.text, 'down')
    self.assertEqual(obj_false.text, 'normal')
    self.assertEqual(dict_rebind.text, 'down')
    self.assertEqual(dict_false.text, 'Unset')
    self.assertEqual(alias_rebind.text, 'down')

    button.state = 'normal'
    Clock.tick()
    self.assertEqual(obj.text, 'normal')
    self.assertEqual(obj_false.text, 'normal')
    self.assertEqual(dict_rebind.text, 'normal')
    self.assertEqual(dict_false.text, 'Unset')
    self.assertEqual(alias_rebind.text, 'normal')

    obj.button = None
    obj_false.button = None
    dict_rebind.button.button = None
    dict_false.button.button = None
    alias_rebind.button = None
    Clock.tick()
    self.assertEqual(obj.text, 'Unset')
    self.assertEqual(obj_false.text, 'Unset')
    self.assertEqual(dict_rebind.text, 'Unset')
    self.assertEqual(dict_false.text, 'Unset')
    self.assertEqual(alias_rebind.text, 'Unset')


@pytest.mark.parametrize('set_name', [True, False])
def test_color_property(self, set_name):
    from kivy.properties import ColorProperty

    color = ColorProperty()
    if set_name:
        color.set_name(wid, 'color')
        color.link_eagerly(wid)
    else:
        color.link(wid, 'color')
        color.link_deps(wid, 'color')
    self.assertEqual(color.get(wid), [1, 1, 1, 1])

    color2 = ColorProperty()
    if set_name:
        color2.set_name(wid, 'color2')
        color2.link_eagerly(wid)
    else:
        color2.link(wid, 'color2')
        color2.link_deps(wid, 'color2')
    self.assertEqual(color2.get(wid), [1, 1, 1, 1])

    color.set(wid, 'yellow')
    self.assertEqual(color.get(wid), [1.0, 1.0, 0.0, 1.0])

    color.set(wid, "#00ff00")
    self.assertEqual(color.get(wid), [0, 1, 0, 1])

    color.set(wid, "#7f7fff7f")
    self.assertEqual(color.get(wid)[0], 127 / 255.)
    self.assertEqual(color.get(wid)[1], 127 / 255.)
    self.assertEqual(color.get(wid)[2], 1)
    self.assertEqual(color.get(wid)[3], 127 / 255.)

    color.set(wid, (1, 1, 0))
    self.assertEqual(color.get(wid), [1, 1, 0, 1])
    color.set(wid, (1, 1, 0, 0))
    self.assertEqual(color.get(wid), [1, 1, 0, 0])

    color.set(wid, [1, 1, 1, 1])
    color_value = color.get(wid)
    color_value[0] = 0.5
    self.assertEqual(color.get(wid), [0.5, 1, 1, 1])

    self.assertEqual(color2.get(wid), [1, 1, 1, 1])
    color2.set(wid, color.get(wid))
    self.assertEqual(color2.get(wid), [0.5, 1, 1, 1])

    color.set(wid, [1, 1, 1, 1])
    color_value = color.get(wid)
    color_value[:] = [0, 1, 0, 1]
    self.assertEqual(color.get(wid), [0, 1, 0, 1])


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_without_setter(self, watch_before_use):
    from kivy.properties import AliasProperty

    expected_value = 5

    class CustomAlias(EventDispatcher):

        def _get_prop(self):
            self.getter_called += 1
            return expected_value

        prop = AliasProperty(_get_prop, None, watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.getter_called = 0

    # Initial checks
    wid = CustomAlias()
    self.assertEqual(wid.getter_called, 0)

    # Get value, should call getter once
    value = wid.prop
    self.assertEqual(value, expected_value)
    self.assertEqual(wid.getter_called, 1)

    # Setter should raise an AttributeError
    self.assertRaises(AttributeError, partial(setattr, wid, 'prop', 1))


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property(self, watch_before_use):
    from kivy.properties import AliasProperty

    class CustomAlias(EventDispatcher):

        def _get_prop(self):
            self.getter_called += 1

        def _set_prop(self, value):
            self.setter_called += 1

        prop = AliasProperty(
            _get_prop, _set_prop, watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.getter_called = 0
            self.setter_called = 0
            self.callback_called = 0

    def callback(widget, value):
        widget.callback_called += 1

    # Initial checks
    wid = CustomAlias()
    wid.bind(prop=callback)
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 0)
    self.assertEqual(wid.callback_called, 0)

    # Set property, should call setter to set the value
    # Getter and callback should not be called because `_set_prop` doesn't
    # returns True
    wid.prop = 1
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 1)
    self.assertEqual(wid.callback_called, 0)

    # Set property to same value as before, should only call setter
    wid.prop = 1
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 2)
    self.assertEqual(wid.callback_called, 0)

    # Get value of the property, should call getter once
    self.assertEqual(wid.prop, None)
    self.assertEqual(wid.getter_called, 1)
    self.assertEqual(wid.setter_called, 2)
    self.assertEqual(wid.callback_called, 0)


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_cache_true(self, watch_before_use):
    from kivy.properties import AliasProperty

    expected_value = 5

    class CustomAlias(EventDispatcher):

        def _get_prop(self):
            self.getter_called += 1
            return expected_value

        def _set_prop(self, value):
            self.setter_called += 1
            return True

        prop = AliasProperty(
            _get_prop, _set_prop, cache=True, watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.getter_called = 0
            self.setter_called = 0

    # Initial checks
    wid = CustomAlias()
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 0)

    # Get value of the property, should call getter once
    value = wid.prop
    self.assertEqual(value, expected_value)
    self.assertEqual(wid.getter_called, 1)
    self.assertEqual(wid.setter_called, 0)

    # Get value of the property, should return cached value
    # Getter should not be called
    value = wid.prop
    self.assertEqual(value, expected_value)
    self.assertEqual(wid.getter_called, 1)
    self.assertEqual(wid.setter_called, 0)

    # Set value of property, should call getter and setter
    wid.prop = 10
    value = wid.prop
    self.assertEqual(value, expected_value)
    self.assertEqual(wid.setter_called, 1)
    self.assertEqual(wid.getter_called, 2)


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_with_bind(self, watch_before_use):
    from kivy.properties import NumericProperty, AliasProperty

    class CustomAlias(EventDispatcher):

        x = NumericProperty(0)
        width = NumericProperty(100)

        def get_right(self):
            return self.x + self.width

        def set_right(self, value):
            self.x = value - self.width

        right = AliasProperty(
            get_right, set_right, bind=('x', 'width'),
            watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.callback_called = 0

    # Assert values when setting x, width or right properties
    wid = CustomAlias()
    self.assertEqual(wid.right, 100)
    wid.x = 500
    self.assertEqual(wid.right, 600)
    wid.width = 50
    self.assertEqual(wid.right, 550)
    wid.right = 100
    self.assertEqual(wid.width, 50)
    self.assertEqual(wid.x, 50)

    def callback(widget, value):
        widget.callback_called += 1

    wid.bind(right=callback)

    # Callback should be called only when property changes
    wid.x = 100
    self.assertEqual(wid.callback_called, 1)
    wid.x = 100
    self.assertEqual(wid.callback_called, 1)
    wid.width = 900
    self.assertEqual(wid.callback_called, 2)
    wid.right = 700
    self.assertEqual(wid.callback_called, 3)
    wid.right = 700
    self.assertEqual(wid.callback_called, 3)


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_with_force_dispatch_true(self, watch_before_use):
    from kivy.properties import AliasProperty

    class CustomAlias(EventDispatcher):

        def _get_prop(self):
            self.getter_called += 1

        def _set_prop(self, value):
            self.setter_called += 1

        prop = AliasProperty(
            _get_prop, _set_prop, force_dispatch=True,
            watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.getter_called = 0
            self.setter_called = 0
            self.callback_called = 0

    def callback(widget, value):
        widget.callback_called += 1

    # Initial checks
    wid = CustomAlias()
    wid.bind(prop=callback)
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 0)
    self.assertEqual(wid.callback_called, 0)

    # Set property, should call setter to set the value and getter to
    # to get the value for dispatch call
    wid.prop = 1
    self.assertEqual(wid.getter_called, 1)
    self.assertEqual(wid.setter_called, 1)
    self.assertEqual(wid.callback_called, 1)

    # Set property to same value as before, setter and getter and callback
    # are called
    wid.prop = 1
    self.assertEqual(wid.getter_called, 2)
    self.assertEqual(wid.setter_called, 2)
    self.assertEqual(wid.callback_called, 2)


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_cache_true_with_bind(self, watch_before_use):
    from kivy.properties import NumericProperty, AliasProperty

    class CustomAlias(EventDispatcher):

        base_value = NumericProperty(1)

        def _get_prop(self):
            self.getter_called += 1
            return self.base_value * 2

        def _set_prop(self, value):
            self.base_value = value / 2

        prop = AliasProperty(_get_prop, _set_prop,
                             bind=('base_value',),
                             cache=True, watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.getter_called = 0

    # Initial checks
    wid = CustomAlias()
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.base_value, 1)
    self.assertEqual(wid.getter_called, 0)

    # Change the base value, should trigger an update for the cache
    wid.base_value = 4
    self.assertEqual(wid.getter_called, int(watch_before_use))

    # Now read the value again, should use the cache
    self.assertEqual(wid.prop, 8)
    self.assertEqual(wid.getter_called, 1)

    # Change the prop itself, should trigger an update for the cache
    wid.prop = 4
    self.assertEqual(wid.getter_called, 2)
    self.assertEqual(wid.base_value, 2)
    self.assertEqual(wid.prop, 4)
    self.assertEqual(wid.getter_called, 2)


@pytest.mark.parametrize('watch_before_use', [True, False])
def test_alias_property_cache_true_force_dispatch_true(self, watch_before_use):
    from kivy.properties import AliasProperty

    class CustomAlias(EventDispatcher):

        def _get_prop(self):
            self.getter_called += 1
            return self.base_value * 2

        def _set_prop(self, value):
            self.setter_called += 1
            self.base_value = value / 2
            return True

        prop = AliasProperty(
            _get_prop, _set_prop, cache=True, force_dispatch=True,
            watch_before_use=watch_before_use)

        def __init__(self, **kwargs):
            super(CustomAlias, self).__init__(**kwargs)
            self.base_value = 1
            self.getter_called = 0
            self.setter_called = 0
            self.callback_called = 0

    def callback(widget, value):
        widget.callback_called += 1

    wid = CustomAlias()
    wid.bind(prop=callback)

    # Initial checks
    self.assertEqual(wid.base_value, 1)
    self.assertEqual(wid.getter_called, 0)
    self.assertEqual(wid.setter_called, 0)
    self.assertEqual(wid.callback_called, 0)

    # Set alias property some value, should call setter and then getter to
    # pass the value to callback
    wid.prop = 16
    self.assertEqual(wid.base_value, 8)
    self.assertEqual(wid.getter_called, 1)
    self.assertEqual(wid.setter_called, 1)
    self.assertEqual(wid.callback_called, 1)

    # Same as the step above, should call setter, getter and callback
    wid.prop = 16
    self.assertEqual(wid.base_value, 8)
    self.assertEqual(wid.getter_called, 2)
    self.assertEqual(wid.setter_called, 2)
    self.assertEqual(wid.callback_called, 2)

    # Get the value of property, should use cached value
    value = wid.prop
    self.assertEqual(value, 16)
    self.assertEqual(wid.getter_called, 2)
    self.assertEqual(wid.setter_called, 2)
    self.assertEqual(wid.callback_called, 2)


def test_dictproperty_is_none():
    from kivy.properties import DictProperty

    d1 = DictProperty(None)
    d1.set_name(wid, 'd1')
    d1.link_eagerly(wid)
    assert d1.get(wid) is None

    d2 = DictProperty({'a': 1, 'b': 2}, allownone=True)
    d2.set_name(wid, 'd2')
    d2.link_eagerly(wid)
    d2.set(wid, None)
    assert d2.get(wid) is None


def test_listproperty_is_none():
    from kivy.properties import ListProperty

    l1 = ListProperty(None)
    l1.set_name(wid, 'l1')
    l1.link_eagerly(wid)
    assert l1.get(wid) is None

    l2 = ListProperty([1, 2, 3], allownone=True)
    l2.set_name(wid, 'l2')
    l2.link_eagerly(wid)
    l2.set(wid, None)
    assert l2.get(wid) is None


def test_numeric_property_dp(kivy_metrics):
    from kivy.event import EventDispatcher
    from kivy.properties import NumericProperty
    kivy_metrics.density = 1

    class Number(EventDispatcher):

        with_dp = NumericProperty(5)

        no_dp = NumericProperty(10)

        default_dp = NumericProperty('10dp')

    number = Number()
    counter = {'with_dp': 0, 'no_dp': 0, 'default_dp': 0}

    def callback(name, *args):
        counter[name] += 1

    number.fbind('with_dp', callback, 'with_dp')
    number.fbind('no_dp', callback, 'no_dp')
    number.fbind('default_dp', callback, 'default_dp')

    assert not counter['with_dp']
    assert not counter['no_dp']
    assert not counter['default_dp']
    assert number.with_dp == 5
    assert number.no_dp == 10
    assert number.default_dp == 10

    number.with_dp = 10
    assert counter['with_dp'] == 1
    assert number.with_dp == 10

    kivy_metrics.density = 2

    assert counter['with_dp'] == 1
    assert not counter['no_dp']
    assert counter['default_dp'] == 1
    assert number.with_dp == 10
    assert number.no_dp == 10
    assert number.default_dp == 20

    number.with_dp = '20dp'
    number.no_dp = 20

    assert counter['with_dp'] == 2
    assert counter['no_dp'] == 1
    assert counter['default_dp'] == 1
    assert number.with_dp == 40
    assert number.no_dp == 20
    assert number.default_dp == 20

    kivy_metrics.density = 1

    assert counter['with_dp'] == 3
    assert counter['no_dp'] == 1
    assert counter['default_dp'] == 2
    assert number.with_dp == 20
    assert number.no_dp == 20
    assert number.default_dp == 10


def test_variable_list_property_dp_default(kivy_metrics):
    from kivy.event import EventDispatcher
    from kivy.properties import VariableListProperty
    kivy_metrics.density = 1

    class Number(EventDispatcher):

        a = VariableListProperty(['10dp', (20, 'dp'), 3, 4.0])

    number = Number()
    counter = 0

    def callback(name, *args):
        nonlocal counter
        counter += 1

    number.fbind('a', callback)
    assert list(number.a) == [10, 20, 3, 4]
    assert not counter

    kivy_metrics.density = 2

    assert counter == 1
    assert list(number.a) == [20, 40, 3, 4]

    kivy_metrics.density = 1

    assert counter == 2
    assert list(number.a) == [10, 20, 3, 4]


def test_variable_list_property_dp(kivy_metrics):
    from kivy.event import EventDispatcher
    from kivy.properties import VariableListProperty
    kivy_metrics.density = 1

    class Number(EventDispatcher):

        a = VariableListProperty([0, 20, 3, 4])

    number = Number()
    counter = 0

    def callback(name, *args):
        nonlocal counter
        counter += 1

    number.fbind('a', callback)
    assert list(number.a) == [0, 20, 3, 4]
    assert not counter

    number.a = ['10dp', (20, 'dp'), 3, 4.0]
    assert list(number.a) == [10, 20, 3, 4]
    assert counter == 1

    kivy_metrics.density = 2

    assert counter == 2
    assert list(number.a) == [20, 40, 3, 4]

    kivy_metrics.density = 1

    assert counter == 3
    assert list(number.a) == [10, 20, 3, 4]


def test_property_duplicate_name():
    from kivy.event import EventDispatcher
    from kivy.properties import ObjectProperty

    class Event(EventDispatcher):

        a = ObjectProperty(5)

    event = Event()
    counter = 0
    counter2 = 0

    def callback(*args):
        nonlocal counter
        counter += 1

    def callback2(*args):
        nonlocal counter2
        counter2 += 1

    event.fbind('a', callback)

    event.create_property('a', None)
    event.fbind('a', callback2)

    event.a = 12
    assert not counter
    assert counter2 == 1


def test_property_rename_duplicate():
    from kivy.event import EventDispatcher
    from kivy.properties import ObjectProperty

    class Event(EventDispatcher):

        b = ObjectProperty(5)
        a = b

    event = Event()
    counter = 0
    counter2 = 0

    def callback(*args):
        nonlocal counter
        counter += 1

    def callback2(*args):
        nonlocal counter2
        counter2 += 1

    event.fbind('a', callback)
    event.fbind('b', callback2)

    event.a = 12
    assert counter == 1
    assert counter2 == 1
    assert event.a == 12
    assert event.b == 12

    event.b = 14
    assert counter == 2
    assert counter2 == 2
    assert event.a == 14
    assert event.b == 14


def test_override_prop_inheritance():
    from kivy.event import EventDispatcher
    from kivy.properties import ObjectProperty, AliasProperty
    counter = 0

    class Parent(EventDispatcher):

        prop = ObjectProperty()

    class Child(Parent):

        def inc(self, *args):
            nonlocal counter
            counter += 1
            return counter

        prop = AliasProperty(inc)

    parent = Parent()
    child = Child()

    parent.prop = 44
    assert parent.prop == 44
    assert counter == 0
    assert child.prop == 1
    assert counter == 1
    assert parent.prop == 44
    assert isinstance(parent.property('prop'), ObjectProperty)
    assert isinstance(child.property('prop'), AliasProperty)


@pytest.mark.parametrize('by_val', [True, False])
def test_manually_create_property(by_val):
    from kivy.event import EventDispatcher
    from kivy.properties import StringProperty

    class Event(EventDispatcher):
        pass

    event = Event()
    assert not hasattr(event, 'a')
    if by_val:
        event.create_property('a', 'hello')
    else:
        event.apply_property(a=StringProperty('hello'))
    args = 0

    def callback(obj, val):
        nonlocal args
        args = obj, val

    event.fbind('a', callback)
    assert event.a == 'hello'
    event.a = 'bye'
    assert event.a == 'bye'
    assert args == (event, 'bye')

    event2 = Event()
    assert event2.a == 'hello'
    event2.fbind('a', callback)
    event2.a = 'goodbye'
    assert event2.a == 'goodbye'
    assert args == (event2, 'goodbye')


def test_inherit_property():
    from kivy.event import EventDispatcher
    from kivy.properties import StringProperty

    class Event(EventDispatcher):

        a = StringProperty('hello')

    class Event2(Event):

        b = StringProperty('hello2')

    event = Event2()
    args = 0

    def callback(obj, val):
        nonlocal args
        args = obj, val

    event.fbind('a', callback)
    event.fbind('b', callback)
    assert event.a == 'hello'
    assert event.b == 'hello2'

    event.a = 'bye'
    assert event.a == 'bye'
    assert args == (event, 'bye')

    event.b = 'goodbye'
    assert event.b == 'goodbye'
    assert args == (event, 'goodbye')


def test_unknown_property():
    from kivy.properties import NumericProperty

    class MyWidget(EventDispatcher):
        width = NumericProperty(0)

    with pytest.raises(TypeError) as cm:
        MyWidget(width=12, unkn="abc")
    assert "Properties ['unkn'] passed to __init__ may not be existing " \
           "property names. Valid properties are ['width']" \
           == str(cm.value)


def test_known_property_multiple_inheritance():

    class Behavior:
        def __init__(self, name):
            print(f'Behavior: {self}, name={name}')
            super().__init__()

    class Widget2(Behavior, EventDispatcher):
        pass

    class Widget3(EventDispatcher, Behavior):
        pass

    with pytest.raises(TypeError) as cm:
        EventDispatcher(name='Pasta')
    assert "Properties ['name'] passed to __init__ may not be existing" \
           in str(cm.value)

    Widget2(name='Pasta')  # does not raise a ValueError
    Widget3(name='Pasta')  # does not raise a ValueError


def test_pass_other_typeerror():

    class Behavior:
        def __init__(self, name):
            super().__init__()
            raise TypeError("this is a typeerror unrelated to object")

    class Widget2(Behavior, EventDispatcher):
        pass

    class Widget3(EventDispatcher, Behavior):
        pass

    for cls in [Widget2, Widget3]:
        with pytest.raises(TypeError) as cm:
            cls(name='Pasta')
        assert "this is a typeerror unrelated to object" == str(cm.value)


def test_object_init_error():  # the above 3 test rely on this
    class TestCls(object):
        def __init__(self, **kwargs):
            super(TestCls, self).__init__(**kwargs)

    with pytest.raises(TypeError) as cm:
        TestCls(name='foo')
    assert str(cm.value).startswith("object.__init__() takes")
