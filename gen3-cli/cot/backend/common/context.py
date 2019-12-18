import os
import string
from .fsutils import ContextSearch, Search


class ContextError(Exception):
    pass


class NoLevelFileError(ContextError):
    def __init__(self, filename):
        super().__init__("Can't find level file {}".format(filename))


class ContextProps:
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return None

    def __str__(self):
        props_str = ""
        for key, value in self.__dict__.items():
            props_str += "  {}={}\n".format(key, value)
        if props_str:
            return props_str
        return "  None"


class attrdict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name):
        return super().__getitem__(name)

    def __setattr__(self, name, value):
        super().__setitem__(name, value)


class Context:

    levels = attrdict()

    @property
    def dir(self):
        return self.__dir

    @dir.setter
    def dir(self, value):
        value = os.path.normcase(value)
        if not os.path.isabs(value):
            raise ValueError('{} is not abs path'.format(value))
        if not os.path.isdir(value):
            raise ValueError('{} is not dir'.format(value))
        self.__dir = value
        self.__search = ContextSearch(self.__dir)
        self.__try_to_set_root()
        self.__try_to_set_tenant()

    @property
    def root(self):
        return self.__root

    @property
    def tenant(self):
        return self.__tenant

    @property
    def account(self):
        return self.__account

    @property
    def search(self):
        return self.__search

    def __init__(self, dir, account=None):
        self.dir = dir
        self.props = ContextProps()
        self.__account = account
        if hasattr(self, 'filename'):
            self.__check_level_filename()
            self.setup()

    def __check_level_filename(self):
        if not self.search.isfile(self.filename):
            raise NoLevelFileError(self.filename)

    def __try_to_set_root(self):
        self.__root = os.path.dirname(self.__search.upwards(self.levels.root.filename))
        if not self.__root:
            raise ValueError('Unable to find {} in {} or its parents'.format(self.levels.root.filename, self.__dir))

    def __try_to_set_account(self):
        found = Search.downwards(self.root, self.levels.account.filename)
        if not found:
            raise ContextError('No accounts found')
        selected_account = None
        found_accounts = []
        for account_filename in found:
            account_level_dir = self.levels.account(os.path.basename(account_filename))
            try:
                account = self.levels.account(account_level_dir)
                found_accounts.append(account)
                if self.account and account.props.name == self.account:
                    selected_account = account
            except ContextError as e:
                raise ContextError('Corrupted account found in {}'.format(account_level_dir)) from e
        if self.account is not None:
            if selected_account is None:
                raise ContextError("Can't find account {}".format(self.account))
            else:
                self.account = account
        else:
            if len(found_accounts) > 1:
                raise ContextError("Can't automatically determine which account to use. Please specify account name.")
            else:
                self.account = found_accounts[0]

    def __try_to_set_tenant(self):
        found = Search.downwards(self.root, self.levels.tenant.filename)
        if not found:
            raise ContextError('Tenant not found')

    def __str__(self):
        template = "level: $name\ndir: $dir\nprops:\n$props"
        return string.Template(template).substitute(
            name=self.name,
            dir=self.dir,
            props=self.props
        )


class LevelMetaclass(type):
    def __init__(cls, name, bases, dct):
        bases[bases.index(Context)]
        Context.levels[dct['name']] = cls


class SegmentLevel(Context, metaclass=LevelMetaclass):

    name = 'segment'
    filename = 'segment.json'

    def setup(self):
        if not self.search.isfile(self.filename):
            raise NoLevelFileError(self.filename)
        self.props.segment = self.search.basename(up=1)
        if self.search.isfile(self.levels.environment.filename, up=1):
            self.dir = self.search.parent(up=1)
        else:
            self.props.environment = self.props.segment
            self.props.segment = 'default'
            self.dir = self.search.parent(up=2)


class EnvironmentLevel(Context, metaclass=LevelMetaclass):

    name = 'environment'
    filename = 'environment.json'

    def setup(self):
        if not self.search.isfile(self.filename):
            raise NoLevelFileError(self.filename)
        self.props.environment = self.search.basename()
        self.dir = self.search.parent(up=2)


class AccountLevel(Context, metaclass=LevelMetaclass):

    name = 'account'
    filename = 'account.json'

    def get_account_name_from_dirname(self):
        prefix = os.path.join(self.root, 'accounts')
        suffix = 'config'
        self.props.name = Search.cut(self.dir, prefix, suffix)

    def load_account_json(self):
        pass

    def setup(self):
        self.get_account_name_from_dirname()


class TenantLevel(Context, metaclass=LevelMetaclass):
    name = 'tenant'
    filename = 'tenant.json'


class ProductLevel(Context, metaclass=LevelMetaclass):

    name = 'product'
    filename = 'product.json'

    def setup(self):
        product = self.search.basename()
        if product == 'config':
            self.props.product = self.search.basename(up=1)
        else:
            self.props.product = product


class IntegratorLevel(Context, metaclass=LevelMetaclass):

    name = 'integrator'
    filename = 'integrator.json'

    def setup(self):
        self.props.integrator = self.search.basename()


class RootLevel(Context, metaclass=LevelMetaclass):

    name = 'root'
    filename = 'root.json'

    def setup(self):
        pass


def Level(dir):
    for level in Context.levels:
        try:
            return Context.levels[level](dir)
        except ContextError:
            pass
    return None


# print(RootLevel('/var/opt/codeontap'))
# print(AccountLevel('/var/opt/codeontap/accounts/account/config'))
