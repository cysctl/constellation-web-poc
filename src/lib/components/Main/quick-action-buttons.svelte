<script lang="ts">
	import { wsStore } from '$lib/stores/websocket.svelte';
	import { satelliteStore } from '$lib/stores/satellites.svelte';

	const buttons = ['Initialize', 'Launch', 'Land', 'Start', 'Stop', 'Shutdown'];

	function sendToAll(label: string) {
		const cmd = label.toLowerCase();

		for (const sat of satelliteStore.list) {
			const target = `${sat.type}.${sat.name}`;

			if (cmd === 'start') {
				wsStore.sendCommand(cmd, target, 'RUN_001');
			} else {
				wsStore.sendCommand(cmd, target);
			}
		}
	}
</script>

<div class="hidden flex-wrap items-center gap-2 md:flex">
	<span class="text-sm text-muted-foreground select-none">All:</span>
	{#each buttons as label}
		<button
			class="cursor-pointer rounded-lg px-2 py-1 text-sm text-muted-foreground transition-colors select-none hover:bg-border active:scale-95"
			onclick={() => sendToAll(label)}
		>
			{label}
		</button>
	{/each}
</div>
