import { ChatInputCommandInteraction } from 'discord.js';
import {
  createAudioPlayer,
  createAudioResource,
  CreateVoiceConnectionOptions,
  joinVoiceChannel,
  JoinVoiceChannelOptions,
} from '@discordjs/voice';
import { parseNotes } from '../beep/parser';
import tmp from 'tmp';
import { generate } from '../beep/generator';

export const playHandler = async (
  interaction: any,
): Promise<void> => {
  const input = interaction.options.getString('input');

  if (!interaction.member.voice.channel) {
    await interaction.reply({content: 'You must be in a voice channel to use this', ephemeral: true});
  }

  await interaction.reply({ content: `Playing: ${input}` });

  console.log(`Playing ${input}`);
  const file = tmp.tmpNameSync({ postfix: '.wav' });
  const notes = parseNotes(input);
  await generate(file, notes);

  console.log(`Generated ${file}`);

  const connection = joinVoiceChannel(<
    CreateVoiceConnectionOptions & JoinVoiceChannelOptions
  >{
    channelId: interaction.member.voice.channelId,
    guildId: interaction.channel.guild.id,
    adapterCreator: interaction.channel.guild.voiceAdapterCreator,
    selfDeaf: false,
    selfMute: false,
  });

  console.log(`Joined ${connection.joinConfig.channelId}`);

  const player = createAudioPlayer();
  connection.subscribe(player);

  const resource = createAudioResource(file);
  player.play(resource);
};
