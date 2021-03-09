#include <iostream>
#include <fstream>
#include <algorithm>
#include "bmi_doc_scal.h"
using namespace std;
BMI_doc_scal::BMI_doc_scal(Seed _seed,
        Dataset *_documents,
        int _num_threads,
        int _training_iterations, int _N, vector<pair<string, int>> &seed_judgments)
    :BMI(_seed, _documents, _num_threads, -1, false, _training_iterations, false)
{
    N = _N;
    T = N;
    R = 0;
    judgments_per_iteration = B;
    for(auto &seed_judgment: seed_judgments){
        auto doc_index = documents->get_index(seed_judgment.first);
        if (doc_index != documents->NPOS) {
            add_to_training_cache(documents->get_index(seed_judgment.first), seed_judgment.second);
        } else {
            cerr << "Document with ID " << seed_judgment.first << " not found." << endl;
        }
    }
    perform_iteration();
    stratums.push_back(vector<pair<int, float>>());
    for(auto doc_id: judgment_queue){
        cerr<<"Stratum pair (docid:score): ("<< documents->get_id(doc_id.first) << ": " << to_string(doc_id.second) + ")" <<endl;
        stratums.back().push_back(make_pair(doc_id.first, doc_id.second));
    }
    B = B + ceil(B/10.0);
}

void BMI_doc_scal::record_judgment_batch(vector<pair<string, int>> _judgments){
    lock_guard<mutex> lock(judgment_list_mutex);
    for(const auto &judgment: _judgments){
        size_t id = documents->get_index(judgment.first);
        if (id != documents->NPOS) {
            add_to_training_cache(id, judgment.second);
            for(int i = (int)judgment_queue.size() - 1; i >= 0; i--){
                if(judgment_queue[i].first == id){
                    judgment_queue.erase(judgment_queue.begin() + i);
                    if(judgment.second > 0) R++;
                    break;
                }
            }
        } else {
            cerr << "Document with ID " << judgment.first << " not found." << endl;
        }
    }

    if(judgment_queue.size() == 0){
        cerr<<"Refreshing"<<endl;
        cerr<<"R = "<<R<<endl;
        if(R >= T) {
            T <<= 1;
            cerr<<"Doubling T to "<<T<<endl;
        }
        cerr<<"Batch Size = "<<B<<endl;
        judgments_per_iteration = B;
        auto batch = perform_training_iteration();
        stratums.push_back(vector<pair<int,float>>());
        for(pair<int,float> doc_id_score: batch){
            cerr<<"Stratum pair (docid:score): ("<< documents->get_id(doc_id_score.first) << ": " << to_string(doc_id_score.second) + ")" <<endl;
            stratums.back().push_back(doc_id_score);
        }

        n = ceil(B*N/(float)T);
        cerr<<"Sampling "<<n<<" documents"<<endl;
        vector<int> selector(batch.size());
        for(int i = 0; i < selector.size(); i++)
            selector[i] = (i < n?1:0);
        shuffle(batch.begin(), batch.end(), rand_generator);
        for(int i = 0; i < batch.size(); i++){
            if(selector[i]) judgment_queue.push_back(batch[i]);
            else judgments[batch[i].first] = -2;
        }
        B = B + ceil(B/10.0);
    }
}

unique_ptr<BMI::StratumInfo> BMI_doc_scal::get_stratum_info(){
    return make_unique<StratumInfo>(stratums.size(), stratums.back().size(), ceil(B*N/(float)T), T, N, R, n);
}

vector<pair<string, float>> BMI_doc_scal::get_stratum_docs(int stratum_number) {
    vector<std::pair<string, float>> ret_results;
    if (0 < stratum_number < ret_results.size()) {
        return ret_results;
    }
    for (auto doc_id_score: stratums[stratum_number-1]) {
        ret_results.push_back({documents->get_id(doc_id_score.first), doc_id_score.second});
    }
    return ret_results;
}