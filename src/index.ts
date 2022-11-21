import { ChatInputCommandInteraction, Events } from 'discord.js';
import { beepHandler } from './handlers/beep';
import { playHandler } from './handlers/play';

const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildVoiceStates
  ],
});

client.on(Events.ClientReady, () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

const handlers = {
  beep: beepHandler,
  play: playHandler,
};

client.on(
  Events.InteractionCreate,
  async (interaction: ChatInputCommandInteraction) => {
    console.log(`Received interaction ${interaction.commandName}`);
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName in handlers) {
      return handlers[interaction.commandName](interaction);
    }

    return interaction.reply({ content: 'Unknown command', ephemeral: true });
  },
);

client.login(process.env.DISCORD_TOKEN).catch(console.error);
