#/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.argparser import ArgParser
from lib.gemini import Gemini
from os import getenv
from lib.multiline_in import MultilineIn
from lib.cmdhandler import CmdHandler
from lib.imageparser import ImageParser
from lib.history import History
from lib.speech import Speech


def get_api_key(varname:str) ->str:
    api_key = getenv(varname)

    if not api_key:
        raise NameError('Error loading %s' % varname)
    else: return api_key


def get_input(history_file) ->str:
    print('\n' + MultilineIn.LABEL_IN, MultilineIn.LABEL_EXIT)
    return MultilineIn.get_user_input(history_file)


def parse_instructions(prompt_text:str) ->tuple[str, str]:
    try:
        command_expand = CmdHandler.get_expand(prompt_text)
    except:
        print(MultilineIn.LABEL_ERROR, 'Shell: Unrecognized command.')
        command_expand = None

    images_locations = CmdHandler.get_file_locations(prompt_text)
    return command_expand, images_locations


def load_images(images_filenames:list) ->list[bytes]:
    try:
        images = [ImageParser.image_resolve(x) for x in images_filenames]
    except:
        print(MultilineIn.LABEL_ERROR, 'Image: Error loading.')
        return
    return images


if __name__ == '__main__':
    # argument parser
    parser = ArgParser()
    parser.set_models(Gemini.AVAILABLE_MODELS)

    args = parser.parse_args()

    # history manager
    if args.clear: History.clear_input()

    # agent initialize
    if args.message or args.interactive:
        feline = Gemini(api=get_api_key(Gemini.API_VARNAME))

        if args.model:
            feline.model = Gemini.AVAILABLE_MODELS[args.model]

        if args.message:
            user_input= ' '.join(args.message)
        else: user_input= ''

        # turn based chat
        loop = True

        while loop:
            History.check_dir()

            if not args.interactive:
                loop=False
            if not user_input:
                user_input = get_input(History.HISTORY_INPUT)

                if not user_input:
                    print()
                    break

            # prompt instructions handler
            command_expand, images_locations = parse_instructions(user_input)
            if command_expand:
                user_input = '%s\n%s' % (user_input, command_expand)

            # image recognition
            if images_locations:
                prompt_contents = load_images(images_locations)

                if not prompt_contents:
                    prompt_contents = user_input
                else:
                    prompt_contents.insert(0, user_input)
        
            # text recognition
            else:
                prompt_contents = user_input

            # text generation
            response_chunks = []
            response = feline.get_chat_stream(prompt_contents)

            print('\n' + MultilineIn.LABEL_OUT)

            for chunk in response:
                print(chunk.text, end='')
                response_chunks.append(chunk)
            
            print('\n---')

            # speech generation
            confirm = input('$> Proceed playback? (y/N): ')
            if confirm.lower() in ('y', 'yes'):

                try:
                    speach_data = feline.generate_speach(response_chunks)
                        
                    wav_dir = str(History.CACHE_DIR)
                    wav_name = Speech.get_wavfilename()
                    wav_path = f'{wav_dir}/{wav_name}'
                    
                    Speech.export_wav(wav_path, speach_data)
                    Speech.play_wav(wav_path)

                except:
                    pass

            user_input = ''
    else:
        parser.print_help()

