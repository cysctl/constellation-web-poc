<script lang="ts">
	import { Ellipsis } from '@lucide/svelte';
	import DropdownMenu from '$lib/components/ui/dropdown-menu.svelte';
	import { wsStore } from '$lib/stores/websocket.svelte';

	interface SatelliteTableItemProps {
		type: string;
		name: string;
		satelliteState: string;
		lastMessage?: string;
		heartbeat?: string;
		lives?: number;
	}

	// The server does not send values like last message, heartbeat, or lives yet.
	// I need to handle the server side first to replace these with real data.
	// I will do this later.
	let {
		type,
		name,
		satelliteState,
		lastMessage = 'Last message content...',
		heartbeat = '-',
		lives = 0
	}: SatelliteTableItemProps = $props();

	let dropdown: DropdownMenu;

	const actions: string[] = [
		'Initialize',
		'Launch',
		'Land',
		'Start',
		'Stop',
		'Shutdown',
		'-',
		'get_name',
		'get_version',
		// 'get_commands',
		'get_state',
		'get_role'
		// 'get_status',
		// 'get_config',
		// 'get_run_id'
	];
</script>

<tr
	class="transition-colors hover:bg-muted/50 [&_td]:text-sm"
	oncontextmenu={(e) => dropdown.open(e)}
>
	<td class="font-mono text-muted-foreground">{type}</td>
	<td class="font-medium">{name}</td>
	<td>
		{satelliteState}
	</td>
	<td>
		{lastMessage}
	</td>
	<td class="text-muted-foreground">{heartbeat}</td>
	<td class="text-muted-foreground">{lives}</td>
	<td class="text-right text-muted-foreground">
		<button
			class="h-fit cursor-pointer rounded-lg p-1 text-muted-foreground transition-colors hover:bg-border active:scale-95"
			onclick={(e) => {
				e.stopPropagation();
				dropdown.open(e);
			}}
		>
			<Ellipsis size={17} />
		</button>
	</td>
</tr>

<DropdownMenu
	bind:this={dropdown}
	deviceType={type}
	deviceName={name}
	items={actions}
	onSelect={(item) => {
		const cmd = item.toLowerCase();
		const target = `${type}.${name}`;

		if (cmd === 'start') {
			// RUN_001 is a placeholder run ID.
			// Hardcoding this for now.
			wsStore.sendCommand(cmd, target, 'RUN_001');
		} else {
			wsStore.sendCommand(cmd, target);
		}
	}}
/>
