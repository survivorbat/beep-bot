import { SlashCommandBuilder } from 'discord.js';

const { REST, Routes } = require('discord.js');

const commands = [
  new SlashCommandBuilder()
    .setName('beep')
    .setDescription('Check connection with the bot'),
  new SlashCommandBuilder()
    .setName('play')
    .setDescription('Play a beep')
    .addStringOption((option) =>
      option.setName('input').setDescription('Beep input').setRequired(true),
    ),
];

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);

(async () => {
  try {
    console.log('Started refreshing application (/) commands.');

    await rest.put(Routes.applicationCommands(process.env.DISCORD_CLIENT_ID), {
      body: commands,
    });

    console.log('Successfully reloaded application (/) commands.');
  } catch (error) {
    console.error(error);
  }
})();
