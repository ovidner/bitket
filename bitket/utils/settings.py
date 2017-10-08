from contextlib import contextmanager

import environ


class PrefixEnv(environ.Env):
    def __init__(self, *args, prefix=None, **kwargs):
        self.var_prefix = prefix or ''
        self.use_prefix = True
        super().__init__(*args, **kwargs)

    def get_value(self, var, *args, **kwargs):
        if self.use_prefix:
            var = self.var_prefix + var
        return super().get_value(var=var, *args, **kwargs)

    @contextmanager
    def unprefixed(self):
        self.use_prefix = False
        yield self
        self.use_prefix = True
