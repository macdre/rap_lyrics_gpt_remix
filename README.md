# rap_lyrics_gpt_remix

## Downloading the lyrics

The genius.py script will search for .txt files in the input directory. The script expects the files to contain a single artist's name per line. 

The script will collect all artists names from all .txt files and then proceed to download lyrics for songs for each of those artists. Note, to avoid api limits, the script uses a MAX_SONGS variable per artist, to cap the number of songs for which lyrics will be downloaded. Feel free to change this limit, but be warned that you can easily run into 500 errors if you get too aggressive. 

The script will then write out a txt file to the intermediate directory for each artist, containing the lyrics to their songs. 

Run the genius.py script like so:
```
python genius.py
```
## Preparing Lyrics for Training

The lyricstotxt.py script parses all lyrics files in the intermediate directory and produces a single corpus.txt file in the output directory. This corpus.txt file will be used in the next steps for training the model.

Run the lyricstotxt.py script like so:
```
python lyricstotxt.py
```

## Training the model

Now to train the model. This step will include reading in the corpus.txt file written out in the previous step, and then saving a trained model in a /tmp/test-rap directory.

Run the run_clm.py script like so:
```
python run_clm.py `
    --output_dir /tmp/test-rap `
    --model_name_or_path gpt2 `
    --config_name ./ `
    --tokenizer_name ./ `
    --train_file=./output/corpus.txt `
    --block_size "512" `
    --do_train `
    --do_eval `
    --per_device_train_batch_size 1 `
    --per_device_eval_batch_size 1 `
    --learning_rate "5e-4" `
    --adam_beta1 "0.9" --adam_beta2 "0.98" --weight_decay "0.01" `
    --num_train_epochs "60" `
    --logging_steps "500" `
    --save_steps "5000" `
    --eval_steps "100"
```

Or, if you are using powershell, use the ps1 script to save terminal space:
```
./run_training.ps1
```

## Running Generation

To generate new outputs from a prompt, run the run_generation.py script like so:
```
python run_generation.py --model_type=gpt2 --model_name_or_path=/tmp/test-rap --length=400
```

Or, if you are using powershell, use the ps1 script to save terminal space:
```
./run_generation.ps1
```