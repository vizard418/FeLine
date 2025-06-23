#/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.argparser import ArgParser
from lib.gemini import Gemini
from lib.multiline_in import MultilineIn
from lib.cmdhandler import CmdHandler
from lib.imageparser import ImageParser
from lib.history import History
from lib.speech import Speech


class FeLine:
    def __init__(self, engine:str):
        if engine == 'gemini':
            self.engine = Gemini()


    def set_model(self, model:str) -> bool:
        if self.engine.AVAILABLE_MODELS.get(model):
            self.engine.model = self.engine.AVAILABLE_MODELS[model]
            return True
        return False


    def clear_cache(self) ->bool:
        try:
            if History.clear_input():
                print(MultilineIn.LABEL_OUT, '~ Input history clean ~')

            if History.delete_wav():
                print(MultilineIn.LABEL_OUT, '~ Deleted WAV files ~')
        except:
            print(MultilineIn.LABEL_ERROR, '~ No files in cache ~')
            return False
        return True


    def get_response(self, contents:str):
        return self.engine.get_chat_stream(contents)


    def generate_speech(self, data:iter, filepath:str) ->bool:
        try:
            speech_data = self.engine.generate_speech(data)
            Speech.export_wav(filepath, speech_data)

        except: return False
        return True


if __name__ == '__main__':
    # argument parser
    parser = ArgParser(*Gemini.AVAILABLE_MODELS)
    args = parser.parse_args()

    # agent initialize
    feline = FeLine(engine='gemini')
    
    if args.clear:
        feline.clear_cache()
    
    if args.model:
        feline.set_model(model=args.model)
    
    prompt_input = ''
    if args.message:
        prompt_input = ' '.join(args.message)


    # need message or --interactive flag
    if not (args.message or args.interactive):
        help_messages = (
            'Please provide me with a message or the -it parameter.',
            'Alternatively, you can use the `--help` parameter'
        )

        print(MultilineIn.LABEL_ERROR, ' '.join(message))
        exit()

    # turn based chat
    loop = True
    while loop:
        History.check_dir()

        if not args.interactive: loop=False
        
        if not prompt_input:
            print('\n' + MultilineIn.LABEL_IN, MultilineIn.LABEL_EXIT)

            prompt_input = MultilineIn.get_user_input(str(History.INPUT_HISTORY))
            if not prompt_input: print(); break


        # prompt instructions handler
        try:
            command_expand = CmdHandler.get_expand(prompt_input)
        except:
            print(MultilineIn.LABEL_ERROR, 'Shell: Unrecognized command.')
            command_expand = None

        if command_expand:
            prompt_input = '%s\n%s' % (prompt_input, command_expand)


        prompt_contents = [prompt_input]

        # image recognition
        images_path= CmdHandler.get_file_locations(prompt_input)
        
        if images_path:
            try:
                images = [ImageParser.image_resolve(x) for x in images_path]
                prompt_contents.append(*images)
            except:
                print(MultilineIn.LABEL_ERROR, 'Image: Error loading.')

        # text generation
        response_chunks = []
        response = feline.get_response(prompt_contents)

        print('\n' + MultilineIn.LABEL_OUT)

        for chunk in response:
            print(chunk.text, end='')
            response_chunks.append(chunk)
            
        print('\n---')

        # speech generation
        if loop or args.speech:
            confirm = input('$> Proceed playback? (y/N): ')

            if confirm.lower() in ('y', 'yes'):
                wav_dir = str(History.DIR_CACHE)
                wav_name = Speech.get_wavfilename()
                wav_realpath = f'{wav_dir}/{wav_name}'

                if feline.generate_speech(response_chunks, wav_realpath):
                    print(MultilineIn.LABEL_OUT, f'-> {wav_realpath}')
                    print('You can use the `aplay` command at the following path')

                else:
                    print(MultilineIn.LABEL_ERROR, 'Speech could not be generated')

        prompt_input = ''

