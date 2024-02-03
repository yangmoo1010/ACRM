from struct_obtain import DataProcessing
from web_model import *
import argparse

def main():
    parser = argparse.ArgumentParser("This is an Antibiotic Combination Recommendation program.\n \
                                        这是一个用于预测抗生素联合用药风险等级的程序")
    parser.add_argument('-i', '--input_data', required=True, default='zhengshijiangnanhaofengjing', 
                        help='The form of input data is a pair of drugs without header.\n \
                        输入一个不带表头的只有两列的药物对数据,两列用逗号或者Tab键分隔,请输入英文名')
    parser.add_argument('-n', '--data_number', required=True, default=0, 
                        help='The max number of your drug pairs. \n \
                            输入文件的最大数据量')
    parser.add_argument('-o', '--output', required=True, default="luohuashijieyoufengjun", 
                        help='output data file')
    args = parser.parse_args()
    
    drug_obj = DataProcessing(args.input_data, args.data_number)
    fingerprint = drug_obj.weary_work()

    prob, risk = AntibioticAI.load_ABCD(fingerprint)
    with open(args.output, 'w') as outs:
        
        for npr in range(len(risk)):
            if "SORRY" in prob[npr]:
                outs.write(str(prob[npr]))
            else:
                outs.write(str(prob[npr])[1:-1])
            outs.write(',' + str(risk[npr]) + '\n')
    print(risk)
    print(prob)

    return 0

if __name__ == '__main__':
    
    main()
