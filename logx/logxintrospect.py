
import inspect


def get_calling_module(name=None, top_level_only=True):
    def top_module(mname):

        if top_level_only:
            return mname.split('.')[0]
        else:
            return mname
    s = inspect.stack()

    def modules_iter():
        for i in range(len(s)):
            m = inspect.getmodule(s[i][0])
            # func_name = s[i][3]
            yield m

    x = next((
        m for m in modules_iter()
        if
        m and
        top_module(m.__name__) != top_module(__name__)),
        None
    )

    return x


def get_nicest_module_name(m=None):
    if not m:
        m = get_calling_module()

    if m:
        _name = m.__name__
    else:
        return '__main__'

    def is_main(name):
        return name == '__main__'

    if is_main(_name):
        if m.__spec__:
            return m.__spec__.name
        else:
            return inspect.getmodulename(inspect.getfile(m))
    else:
        return _name
