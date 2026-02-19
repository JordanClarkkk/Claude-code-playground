# Universe Components

Web Components (custom HTML elements). Use as HTML tags with attributes.
- Property values in quotes are exact strings: `<v-button theme="danger">`
- Listen to events via addEventListener, payload in `event.detail`
- Pass content to slots: `<v-button><v-icon slot="left-icon" name="plus"/></v-button>`

---

## v-avatar

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `size` | "big" "regular" "small" "xsmall" | "regular" | no |
| `type` | "corporation" "person" | "person" | no |
| `url` | string | - | yes |

---

## v-badge

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `background` | "dark" "general" | "general" | no |
| `color` | "accent" "attention" "info" "negative" "neutral" "positive" | "accent" | no |
| `form` | "rounded" "squared" | "rounded" | no |
| `secondary` | boolean | false | no |
| `size` | "regular" "small" | "regular" | no |
| `text` | string | - | yes |

---

## v-button

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `background` | "dark" "general" | "general" | no |
| `disabled` | boolean | false | no |
| `icon-side` | "both" "left" "none" "right" | "none" | no |
| `link` | string | - | no |
| `loading` | boolean | false | no |
| `name` | string | 'Button' | no |
| `secondary` | boolean | false | no |
| `size` | "regular" "small" "xsmall" | "regular" | no |
| `target` | string | - | no |
| `text` | string | '' | no |
| `theme` | "danger" "neutral" "primary" "success" | "primary" | no |
| `type` | "ghost" "inline" "solid" | "solid" | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `buttonClick` | - | - |

### Slots

| Slot | Description |
|------|-------------|
| `left-icon` | Icon to display on the left side of the button text (visible when icon-side="left" or "both") |
| `right-icon` | Icon to display on the right side of the button text (visible when icon-side="right" or "both") |

---

## v-checkbox

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `checked` | boolean | false | no |
| `disabled` | boolean | false | no |
| `state` | "default" "mixed" | "default" | no |
| `text` | string | '' | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `checkboxChange` | - | - |

---

## v-counter

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `disabled` | boolean | false | no |
| `is-focused` | boolean | false | no |
| `label-text` | string | '' | no |
| `max` | number | 100 | no |
| `min` | number | 0 | no |
| `min-width` | number | 64 | no |
| `step` | number | 10 | no |
| `text` | string | - | yes |
| `unit-name` | string | '' | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `counterBlur` | - | - |
| `counterChange` | `string` | Emitted when input loses focus or user presses Enter. Detail contains the final input value as string |
| `counterFocus` | - | - |
| `counterInput` | `string` | Emitted on every keystroke. Detail contains the current input value as string |
| `counterStepDown` | - | Emitted when the minus button is clicked to decrease the value |
| `counterStepUp` | - | Emitted when the plus button is clicked to increase the value |

---

## v-flag

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `iso` | string | - | yes |
| `size` | "large" "medium" "small" | "small" | no |

---

## v-hint

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `background` | "dark" "general" | "general" | no |
| `text` | string | - | yes |
| `theme` | "default" "error" "info" "success" "warning" | "default" | no |

---

## v-icon

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `height` | number | 0 | no |
| `name` | string | - | yes |
| `size` | "huge" "large" "medium" "regular" "small" | "regular" | no |
| `transition` | boolean | false | no |
| `width` | number | 0 | no |

---

## v-icon-button

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `background` | "dark" "general" | "general" | no |
| `disabled` | boolean | false | no |
| `form` | "rounded" "squared" | "squared" | no |
| `loading` | boolean | false | no |
| `name` | string | 'Button' | no |
| `secondary` | boolean | false | no |
| `size` | "regular" "small" "xsmall" | "regular" | no |
| `theme` | "danger" "neutral" "primary" "success" | "primary" | no |
| `type` | "ghost" "inline" "solid" | "solid" | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `iconButtonClick` | - | - |

### Slots

| Slot | Description |
|------|-------------|
| `(default)` | Icon element (v-icon) to display inside the button |

---

## v-loader

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `background` | "dark" "general" | "general" | no |
| `color` | string | - | no |
| `direction` | "horizontal" "vertical" | "vertical" | no |
| `size` | "big" "huge" "regular" "small" | "big" | no |
| `text` | string | '' | no |

---

## v-radio-button

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `checked` | boolean | false | no |
| `disabled` | boolean | false | no |
| `name` | string | 'radio-name' | no |
| `radio-id` | string | 'radio-id' | no |
| `text` | string | '' | no |
| `value` | string | 'radio-value' | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `radioChange` | - | - |

---

## v-radio-button-group

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `current` | string | - | yes |
| `direction` | "horizontal" "vertical" | "vertical" | no |
| `items` | VRadioButton[] | - | yes |
| `name` | string | 'v-radio-button-name' | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `radioGroupChange` | `string` | Emitted when selection changes. Detail contains the value attribute of the selected radio button |

---

## v-range-slider

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `axis-dimension` | number | 0 | no |
| `display-value-tag` | boolean | false | no |
| `max` | number | 100 | no |
| `max-label` | string | '' | no |
| `min` | number | 0 | no |
| `min-label` | string | '' | no |
| `show-axis` | boolean | false | no |
| `show-axis-labels` | boolean | false | no |
| `step` | number | 10 | no |
| `values` | string | [0] | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `rangeChange` | `number[]` | Emitted during drag. Detail contains array of current handle values |
| `rangeChangeEnd` | `number[]` | Emitted when user stops dragging. Detail contains array of final handle values |
| `rangeChangeStart` | `number[]` | Emitted when user starts dragging. Detail contains array of current handle values |

---

## v-tab

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `attention` | boolean | false | no |
| `background` | "dark" "general" | "general" | no |
| `badge-text` | string | - | no |
| `disabled` | boolean | false | no |
| `selected` | boolean | - | no |
| `size` | "big" "regular" "small" | "regular" | no |
| `tab-id` | string | - | no |
| `text` | string | - | yes |
| `type` | "lined" "rounded" | - | yes |
| `with-badge` | boolean | - | no |
| `with-icon` | boolean | - | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `tabClick` | `number` | - |
| `tabKeyDown` | `KeyboardEvent` | - |

### Slots

| Slot | Description |
|------|-------------|
| `(default)` | Icon element (v-icon) to display inside the tab when withIcon is true |

---

## v-tabs

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `background` | "dark" "general" | "general" | no |
| `selected-tab-index` | number | - | yes |
| `size` | "big" "regular" "small" | "regular" | no |
| `tabs` | VTabConfig[] | - | yes |
| `type` | "lined" "rounded" | - | no |
| `with-badge` | boolean | - | no |
| `with-icon` | boolean | - | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `tabsClick` | `number` | Emitted when a tab is clicked or selected via keyboard. Detail contains the index of the selected tab |

### Slots

| Slot | Description |
|------|-------------|
| `icon0` | Icon for the first tab (index 0) |
| `icon1` | Icon for the second tab (index 1) |
| `icon2` | Icon for the third tab (index 2) |
| `icon{n}` | Icon for tab at index n (pattern continues for additional tabs) |

---

## v-tag

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `as-block` | boolean | false | no |
| `avatar-type` | "corporation" "person" | "person" | no |
| `avatar-url` | string | '' | no |
| `badge-text` | string | '' | no |
| `clickable` | boolean | false | no |
| `color` | "info" "negative" "neutral" "positive" "primary" "warning" "white" | "primary" | no |
| `flag-iso` | string | '' | no |
| `form` | "rounded" "squared" | "rounded" | no |
| `icon-only` | boolean | false | no |
| `icon-side` | "left" "none" "right" | "none" | no |
| `secondary` | boolean | false | no |
| `size` | "regular" "small" | "regular" | no |
| `text` | string | '' | no |
| `type` | "clear-inline" "inline" "solid" | "solid" | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `tagClick` | - | - |

### Slots

| Slot | Description |
|------|-------------|
| `(default)` | Icon element (v-icon) to display inside the tag when iconSide is set |

---

## v-textarea

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `autoresize` | boolean | false | no |
| `disabled` | boolean | false | no |
| `is-focused` | boolean | false | no |
| `label-text` | string | '' | no |
| `maxlength` | number | - | no |
| `monospace` | boolean | false | no |
| `oneline` | boolean | false | no |
| `placeholder` | string | '' | no |
| `text` | string | '' | no |
| `theme` | "default" "error" "light" "success" | "default" | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `textareaBlur` | - | - |
| `textareaClear` | - | - |
| `textareaFocus` | - | - |
| `textareaInput` | `CustomEvent<any>` | Emitted on every input. Detail contains the native input event |
| `textareaKeyDown` | `KeyboardEvent` | - |
| `textareaReady` | - | Emitted when the textarea component has finished loading and is ready for interaction |

---

## v-toggle

### Properties

| Property | Values | Default | Required |
|----------|--------|---------|----------|
| `checked` | boolean | false | no |
| `disabled` | boolean | false | no |
| `label-side` | "left" "right" | "right" | no |
| `label-text` | string | '' | no |
| `loading` | boolean | false | no |
| `with-icons` | boolean | false | no |

### Events

| Event | CustomEvent detail | Description |
|-------|-------------------|-------------|
| `toggleChange` | - | - |

---