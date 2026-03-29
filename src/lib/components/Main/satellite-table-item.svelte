<script lang="ts">
	import { Ellipsis } from '@lucide/svelte';

	interface SatelliteTableItemProps {
		type: string;
		name: string;
		satelliteState: string;
		lastMessage: string;
		heartbeat: string;
		lives: number;
	}

	let { type, name, satelliteState, lastMessage, heartbeat, lives }: SatelliteTableItemProps =
		$props();
</script>

<tr class="transition-colors hover:bg-muted/50 [&_td]:text-sm">
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
		>
			<Ellipsis size={17} />
		</button>
	</td>
</tr>
