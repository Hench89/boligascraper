import os
import time
import pandas as pd


class RawArchive:

    def __init__(self):
        self.list_forsale = f'./archive/list_forsale'
        self.list_sold = f'./archive/list_sold'
        self.estate_forsale = f'./archive/estate_forsale'
        self.estate_sold = f'./archive/estate_sold'
        for f in [self.list_forsale, self.list_sold, self.estate_forsale, self.estate_sold]:
            self.create_folder(f)


    def create_folder(self, folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def save_forsale_list(self, df):
        file_name = time.strftime("%Y%m%d-%H%M%S")
        file_path = f'{self.list_forsale}/{file_name}'
        df.to_csv(file_path, index=False, compression="gzip")


    def save_sold_list(self, df):
        file_name = time.strftime("%Y%m%d-%H%M%S")
        file_path = f'{self.list_sold}/{file_name}'
        df.to_csv(file_path, index=False, compression="gzip")


    def read_forsale_list(self):
        file_path = self.get_latest_file(self.list_forsale)
        df = pd.read_csv(file_path, compression="gzip")
        return df


    def read_sold_list(self):
        file_path = self.get_latest_file(self.list_sold)
        df = pd.read_csv(file_path, compression="gzip")
        return df


    def get_latest_file(self, folder_path: str):
        file_list = os.listdir(folder_path)
        file_list.sort(reverse=True)
        latest_file_path = f'{folder_path}/{file_list[0]}'
        return latest_file_path


    def get_list_freshness(self):
        try:
            latest_file = self.get_latest_file(self.list_forsale)
            age_seconds = time.time() - os.path.getmtime(latest_file)
            age_minutes = int(age_seconds) / 60
            age_hours = age_minutes / 60
            return round(age_hours)
        except Exception:
            return 99


    def get_forsale_list_ids(self):
        df = self.read_forsale_list()
        ids = df['id'].tolist()
        return ids


    def get_forsale_archive_ids(self):
        file_list = os.listdir(self.estate_forsale)
        return file_list


    def save_forsale_estate(self, df: pd.DataFrame, estate_id: str):
        file_path = f'{self.estate_forsale}/{estate_id}'
        df.to_csv(file_path, index=False, compression="gzip")


    def get_sold_list_ids(self):
        df = self.read_sold_list()
        ids = df['estateId'].tolist()
        return ids


    def get_sold_archive_ids(self):
        file_list = os.listdir(self.estate_sold)
        return file_list


    def save_sold_estate(self, df: pd.DataFrame, estate_id: str):
        file_path = f'{self.estate_sold}/{estate_id}'
        df.to_csv(file_path, index=False, compression="gzip")


    def read_all_forsale_estate(self):
        file_names = os.listdir(self.estate_forsale)
        file_paths = [f'{self.estate_forsale}/{x}' for x in file_names]
        dfs = [pd.read_csv(x, compression="gzip") for x in file_paths]
        df = pd.concat(dfs)
        return df


    def read_all_sold_estate(self):
        file_names = os.listdir(self.estate_sold)
        file_paths = [f'{self.estate_forsale}/{x}' for x in file_names]
        dfs = [pd.read_csv(x, compression="gzip") for x in file_paths]
        df = pd.concat(dfs)
        return df
