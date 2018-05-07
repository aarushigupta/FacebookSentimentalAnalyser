

function tokenize(input) {
    return input
        .toLowerCase()
        .replace(/\n/g, ' ')
        .replace(/[.,\/#!$%\^&\*;:{}=_`\"~()]/g, '')
        .split(' ');
};


function analyseSentimentPerceptron(percep_data, phrase, inject, callback) {

    // console.log("Called analyseSentimentPerceptron");

    //     // Parse arguments
    if (typeof phrase === 'undefined') phrase = '';
    if (typeof inject === 'undefined') inject = null;
    if (typeof inject === 'function') callback = inject;
    if (typeof callback === 'undefined') callback = null;

    // Merge
    if (inject !== null) {
        afinn = Object.assign(afinn, inject);
    }

    var weights = percep_data['weights'];
    var bias = percep_data['bias'];
    var unique_words = percep_data['unique_words'];

    var words = tokenize(phrase);

    var unique_words_len = Object.keys(percep_data['unique_words']).length
    var i;
    var one_hot_vector = new Array(unique_words_len);
    for (i = 0; i < unique_words_len; i++){
        one_hot_vector[i] = 0;
    }

    for (i = 0; i < words.length; i++){
        if (words[i] in unique_words){
            one_hot_vector[unique_words[words[i]]] += 1;
        }
    }


    var sum = 0;
    var label = 1;
    for (i = 0; i < unique_words_len; i++){
        sum += one_hot_vector[i] * weights[i];
    }

    sum += bias;


    if (sum < 0){
        label = -1;
    }
    else{
        label = 1;
    }

    if (callback === null) return label;
    process.nextTick(function () {
        callback(null, result);
    });

};

