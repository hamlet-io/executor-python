import os
from .fsutils import ContextSearch, Search, File


class ContextError(Exception):
    pass


class NoLevelFileError(ContextError):
    pass


class NoRootFileError(ContextError):
    pass


class MultipleTenantsFoundError(ContextError):
    pass


class NoTenantFoundError(ContextError):
    pass


class NoAccountsFoundError(ContextError):
    pass


class MultipleAccountsFoundError(ContextError):
    pass


class SpecifiedAccountNotFoundError(ContextError):
    pass


class Context():
    # Enables tenant->account lookup at the init stage
    ACCOUNT_REQUIRED = False
    # Enables tenant lookup at the init stage
    TENANT_REQUIRED = False
    # Context level name
    level_name = None
    # Context level_file
    level_file = None
    # Context level_file directory
    level_file_directory = None

    # Directory used for initializing context instance
    @property
    def directory(self):
        return self.__directory

    # Backend CWD. It can be changed unlike context initialization directory.
    @property
    def cwd(self):
        return self.__cwd

    @cwd.setter
    def cwd(self, value):
        self.__cwd = value

    # Root file directory
    @property
    def root(self):
        return self.__root

    # Context search tied to current directory
    @property
    def search(self):
        return self.__search

    def setup(self):
        pass

    def __init__(self, directory, config=None):
        config = config or {}
        self.config = config
        self.props = {}
        self.__search = ContextSearch(directory)
        self.__directory = directory
        self.__try_to_find_root()
        if self.ACCOUNT_REQUIRED or self.TENANT_REQUIRED:
            self.__try_to_set_tenant()
            if self.ACCOUNT_REQUIRED:
                self.__try_to_set_account()
        if self.level_name:
            self.__try_to_find_level_file()
        self.setup()

    def __try_to_find_root(self):
        found = self.search.upwards(RootLevel.level_file)
        if not found:
            raise NoRootFileError(f"Can't find {RootLevel.level_file} file.")
        self.__root = Search.parent(found, up=1)

    def __try_to_set_account(self):
        # Trying to find account directory in tenant directory(props['tenant'])
        # If there is a single account and suggested account is not set(config['account'])
        # found account will be used by default
        # If suggested account is set(config['account']), try to find account with name == config['account']
        # If no account with that name found raise SpecifiedAccountNotFoundError.
        accounts_directory = Search.parent(self.props['Tenant'], up=1)
        account_suffix = os.path.join('config', AccountLevel.level_file)

        # Each account filepath has common prefix and suffix
        def name_from_path(path):
            return Search.cut(path, prefix=accounts_directory, suffix=account_suffix)

        found = Search.downwards(accounts_directory, AccountLevel.level_file)
        account_name = self.config.get('account')
        account_path = None
        if not found:
            raise NoAccountsFoundError(f"Can't find accounts in {self.props['Tenant']}")
        elif len(found) == 1:
            account_path = found[0]
            if account_name and account_name != name_from_path(account_path):
                raise SpecifiedAccountNotFoundError(f"Can't find account {account_name} in {accounts_directory}")
        else:
            if not account_name:
                raise MultipleAccountsFoundError(
                    f"Multiple account found in {accounts_directory}. Specify account name"
                )
            for account_path in found:
                if account_name == name_from_path(account_path):
                    break
            else:
                raise SpecifiedAccountNotFoundError(f"Can't find account {account_name} in {accounts_directory}")
        self.props["Account"] = Search.parent(account_path, up=2)

    def __try_to_set_tenant(self):
        # Searching for tenant directory. Directory should contain TenantLevel.level_file
        # Multiple tenants not supported at the moment
        found = Search.downwards(self.root, TenantLevel.level_file)
        if not found:
            raise NoTenantFoundError()
        elif len(found) > 1:
            raise MultipleTenantsFoundError()
        else:
            self.props["Tenant"] = Search.parent(found[0], up=1)

    def __try_to_find_level_file(self):
        # Try to find level file, path to which is set by directory + level_file_directory + level_file
        # Used to deremine the correctness of suggested level.
        # If level file not found, raises NoLevelFileError
        level_file_relpath = []
        if self.level_file_directory:
            level_file_relpath.append(self.level_file_directory)
        level_file_relpath.append(self.level_file)
        level_file_path = self.search.isfile(os.path.join(*level_file_relpath))
        if not level_file_path:
            raise NoLevelFileError(f"No level file in {os.path.join(self.directory, *level_file_relpath)}")
        self.level_file_path = level_file_path


class SegmentLevel(Context):

    ACCOUNT_REQUIRED = True

    level_name = 'segment'
    level_file = 'segment.json'

    def setup(self):
        segment = self.search.basename()
        if self.search.isfile(EnvironmentLevel.level_file, up=1):
            self.cwd = self.search.parent(up=1)
            environment = self.search.basename(up=1)
        else:
            environment = segment
            segment = 'default'
            self.cwd = self.search.parent(up=2)
        self.props['Environment'] = environment
        self.props['Segment'] = segment


class EnvironmentLevel(Context):

    ACCOUNT_REQUIRED = True

    level_name = 'environment'
    level_file = 'environment.json'

    def setup(self):
        self.props['Environment'] = self.search.basename()
        self.cwd = self.search.parent(up=2)


class RootLevel(Context):
    level_name = 'root'
    level_file = 'root.json'
    level_file_directory = None


class TenantLevel(Context):
    level_name = 'tenant'
    level_file = 'tenant.json'
    level_file_directory = None


class AccountLevel(Context):

    TENANT_REQUIRED = True

    level_name = 'account'
    level_file = 'account.json'
    level_file_directory = 'config'

    def setup(self):
        self.props.update(File(self.level_file_path).load())


class ProductLevel(Context):

    ACCOUNT_REQUIRED = True

    level_name = 'product'
    level_file = 'product.json'
    level_file_directory = 'config'


class IntegratorLevel(Context):

    name = 'integrator'
    filename = 'integrator.json'

    def setup(self):
        self.props['Integrator'] = self.search.basename()
