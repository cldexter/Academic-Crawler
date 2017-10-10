#! /usr/bin/env python
# coding=utf-8
# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   File Name: lsi_model.py
   Description: 产生LSI模型
   Author: Dexter Chen
   Date：2018-10-09
-------------------------------------------------
   Development Note：
   
-------------------------------------------------
'''

from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize
from gensim import corpora, models, similarities
import logging

word_set_1 = "Animal models are essential for in vivo analysis of Helicobacter-related diseases. Mongolian gerbils are used frequently to study Helicobacter pylori-induced gastritis and its consequences. The presence of some gastric microbiota with a suppressive effect on H. pylori suggests inhibitory gastric bacteria against H. pylori infection. The aim of the present study was to analyse the microbial ecology between H. pylori and the gastric microbiota of Mongolian gerbils. Gastric mucosa samples of H. pylori-negative and -positive gerbils were orally inoculated to five (Group 1) and six (Group 2) gerbils, respectively, and the gerbils were challenged with H. pylori infection. The colonization rate (40 %) of H. pylori in Group 1 gerbils was lower than the rate (67 %) in Group 2 gerbils. Culture filtrate of the gastric mucosa samples of Group 1 gerbils inhibited the in vitro growth of H. pylori. Three lactobacilli species, Lactobacillus reuteri, Lactobacillus johnsonii and Lactobacillus murinus, were isolated by anaerobic culture from the gerbils in Groups 1 and 2, and identified by genomic sequencing. It was demonstrated that the three different strains of lactobacilli exhibited an inhibitory effect on the in vitro growth of H. pylori. The results suggested that lactobacilli are the dominant gastric microbiota of Mongolian gerbils and the three lactobacilli isolated from the gastric mucosa samples with an inhibitory effect on H. pylori might have an anti-infective effect against H. pylori."

word_set_2 = "Gamma-amino butyric acid (GABA) is an active biogenic substance synthesized in plants, fungi, vertebrate animals and bacteria. Lactic acid bacteria are considered the main producers of GABA among bacteria. GABA-producing lactobacilli are isolated from food products such as cheese, yogurt, sourdough, etc. and are the source of bioactive properties assigned to those foods. The ability of human-derived lactobacilli and bifidobacteria to synthesize GABA remains poorly characterized. In this paper, we screened our collection of 135 human-derived Lactobacillus and Bifidobacterium strains for their ability to produce GABA from its precursor monosodium glutamate. Fifty eight strains were able to produce GABA. The most efficient GABA-producers were Bifidobacterium strains (up to 6Â g/L). Time profiles of cell growth and GABA production as well as the influence of pyridoxal phosphate on GABA production were studied for L.Â plantarum 90sk, L.Â brevis 15f, B.Â adolescentis 150 and B.Â angulatum GT102. DNA of these strains was sequenced; the gadB and gadC genes were identified. The presence of these genes was analyzed in 14 metagenomes of healthy individuals. The genes were found in the following genera of bacteria: Bacteroidetes (Bacteroides, Parabacteroides, Alistipes, Odoribacter, Prevotella), Proteobacterium (Esherichia), Firmicutes (Enterococcus), Actinobacteria (Bifidobacterium). These data indicate that gad genes as well as the ability to produce GABA are widely distributed among lactobacilli and bifidobacteria (mainly in L.Â plantarum, L. brevis, B. adolescentis, B. angulatum, B. dentium) and other gut-derived bacterial species. Perhaps, GABA is involved in the interaction of gut microbiota with the macroorganism and the ability to synthesize GABA may be an important feature in the selection of bacterial strains - psychobiotics."

word_set_3 = "Vaginal commensal lactobacilli are considered to contribute significantly to the control of vaginal microbiota by competing with other microflora for adherence to the vaginal epithelium and by producing antimicrobial compounds. However, the molecular mechanisms of symbiotic prokaryotic-eukaryotic communication in the vaginal ecosystem remain poorly understood. Here, we showed that both DNA methylation and histone modifications were associated with expression of the DEFB1 gene, which encodes the antimicrobial peptide human Î²-defensin-1, in vaginal keratinocyte VK2/E6E7 cells. We investigated whether exposure to Lactobacillus gasseri and Lactobacillus reuteri would trigger the epigenetic modulation of DEFB1 expression in VK2/E6E7 cells in a bacterial species-dependent manner. While enhanced expression of DEFB1 was observed when VK2/E6E7 cells were exposed to L. gasseri, treatment with L. reuteri resulted in reduced DEFB1 expression. Moreover, L. gasseri stimulated the recruitment of active histone marks and, in contrast, L. reuteri led to the decrease of active histone marks at the DEFB1 promoter. It was remarkable that distinct histone modifications within the same promoter region of DEFB1 were mediated by L. gasseri and L. reuteri. Therefore, our study suggested that one of the underlying mechanisms of DEFB1 expression in the vaginal ecosystem might be associated with the epigenetic crosstalk between individual Lactobacillus spp. and vaginal keratinocytes."

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

word_list = [word_set_1, word_set_2, word_set_3]

processed_word_list = []

corpus = []

dictionary = corpora.Dictionary(processed_word_list)
stop_words = stopwords.words('english') # 英文停用词
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', "-", "~"] # 英文标点符号

def content_pre(str): # 准备好文本：去停用词、标点、词干化; 输入str，输出集合
    content = str.encode("utf-8")

    word_set = [] # 分词后的
    word_no_punc = [] # 没有标点符号的
    word_no_stop_words = [] # 没有停用词
    word_stemmed = [] # 词干化后的

    word_set = word_tokenize(content) # tokenize

    for word in word_set: # 去掉标点符号
        if word not in stop_words:
            word_no_punc.append(word)

    for word in word_no_punc: # 去掉停用词
        if word not in english_punctuations:
            word_no_stop_words.append(word)

    st = LancasterStemmer() 
    for word in word_no_stop_words: # 词干化
        word_stemmed.append(st.stem(word))

    return word_stemmed

def words_bag(word_list): # 生成词袋；输入预处理的词，输出corpus
    corpus = dictionary.doc2bow(word_list)
    return corpus

def tfidf_model(corpus_list): # 建立tfidf模型； 输入corpus的集合，输出文档向量
    tfidf_model = models.TfidfModel(corpus_list) # 建立tfidf模型, 由多个corpus训练所得
    vector_list = tfidf_model[corpus_list] # 用模型处理 corpus集合
    return vector_list

def lsi_model(vector_list, topic_number): # 建立LSI模型; 输入文档向量，bow
    lsi_model = models.LsiModel(vector_list, id2word=dictionary, num_topics=topic_number) # 建立lsi模型，由多个vector训练所得；topic_number可以主观加入
    lsi_list = lsi_model[vector_list] # 用模型处理 vector集合
    return lsi_list # 输出topic相关度指数

def build_index()


def build_models(corpus_list): # 
