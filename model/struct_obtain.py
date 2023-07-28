# import pubchempy as pcp
from pubchempy import Compound, get_compounds
from rdkit import Chem
from rdkit.Chem import MACCSkeys
import re 
import numpy as np


class DataProcessing:

    def __init__(self, your_data, data_num):

        self.your_data = your_data
        self.data_num = int(data_num)
        self.data_list = []
        self.pattern = r'[,\t]'

    def weary_work(self):

        with open(self.your_data, 'r') as bigdata:
            for big in bigdata.readlines():
                self.data_list.append(re.split(self.pattern, big.strip()))
                print(self.data_list)
            if self.data_num > 100:
                self.pubchem_match_slow(self.data_list)
                #self.pubchem_match_mbfast(self.data_list)
            else:
                # print('begin')
                self.pubchem_match_slow(self.data_list)
            # print("over")
        return self.fingerprints
    
    def pubchem_match_slow(self, drug_list):
        
        self.fingerprints = []
        self.not_found = []

        for n,names in enumerate(drug_list):
                
            compound1 = get_compounds(names[0].lower(), 'name')
            compound2 = get_compounds(names[1].lower(), 'name')
                
            if len(compound1) >= 1 and len(compound2) >= 1: 
                #获取该药物所有可能的smiles中的第一个     
                name_smile1 = compound1[0].isomeric_smiles
                name_smile2 = compound2[0].isomeric_smiles
                #获取该药物smiles的分子指纹
                mol1 = Chem.MolFromSmiles(name_smile1)
                mol2 = Chem.MolFromSmiles(name_smile2)
                fdrug1 = MACCSkeys.GenMACCSKeys(mol1)
                fdrug2 = MACCSkeys.GenMACCSKeys(mol2)
                #变成二进制列表
                temp1 = [int(b1) for b1 in fdrug1]
                temp2 = [int(b2) for b2 in fdrug2]
                # print(len(temp1 + temp2))

                self.fingerprints.append(temp1 + temp2)

            else:
                if len(compound1) < 1 and len(compound2) >= 1:
                    self.fingerprints.append(f'SORRY, {names[0]} IS NO MATCH.')
                elif len(compound2) < 1 and len(compound1) >= 1:
                    self.fingerprints.append(f'SORRY, {names[1]} IS NO MATCH.')
                else:
                    self.fingerprints.append(f'SORRY BOTH {names[0]} AND {names[1]} ARE NO MATCH.')
                self.not_found.append(n)
        # print(self.fingerprints)
        return 0


if __name__ == '__main__': 

    import sys
    your_data = sys.argv[1]
    data_num = sys.argv[2]
    obj = DataProcessing(your_data, data_num)
    fingerprint = obj.weary_work()