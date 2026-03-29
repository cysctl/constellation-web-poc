<script lang="ts">
	interface SatelliteTableItemProps {
		type: string;
		name: string;
		state: string;
		lastMessage: string;
		heartbeat: string;
		lives: number;
	}

	let { type, name, state, lastMessage, heartbeat, lives }: SatelliteTableItemProps = $props();
</script>

<tr class="transition-colors hover:bg-muted/50 [&_td]:text-sm">
	<td class="font-mono text-muted-foreground">{type}</td>
	<td class="font-medium">{name}</td>
	<td>
		{state}
	</td>
	<td>
		{lastMessage}
	</td>
	<td class="text-muted-foreground">{heartbeat}</td>
	<td class="text-muted-foreground">{lives}</td>
	<td class="text-right text-muted-foreground">actions</td>
</tr>
