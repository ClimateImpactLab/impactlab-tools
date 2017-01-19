
import xarray as xr
import metacsv
import datafs
import os


class DataCache(object):

    _api = None
    _data = {}

    @classmethod
    def retrieve(cls, archive_name, api=None):

        if archive_name in cls._data:
            return cls._data[archive_name]

        if api is None:

            if cls._api is None:
                cls._api = datafs.get_api()

            api = cls._api

        archive = api.get_archive(archive_name)

        if archive_name.endswith('.csv'):
            with archive.open() as f:
                data = metacsv.read_csv(f)

        elif os.path.splitext(archive_name)[-1][:3] == '.nc':
            with archive.get_local_path() as fp:
                data = xr.open_dataset(fp).load()

        else:
            raise ValueError('file type not recognized: "{}"'.format(
                archive_name))

        cls._data[archive_name] = data

        return data
