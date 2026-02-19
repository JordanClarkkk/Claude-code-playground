# Ember Components

Glimmer components for Ember.js applications. Use as angle-bracket components with arguments.
- Argument values use `@` prefix in templates: `<VChip @text="Label" @checked={{true}} />`
- Pass actions as arguments: `<VChip @chipChange={{this.handleChange}} />`
- Use named blocks for custom content: `<VModal>...<:content>Custom</:content></VModal>`

---

## v-banner-container

Container for displaying banner messages. Works with the `bannerController` service.

### Arguments

*No arguments*

### Blocks

| Name | Description |
|------|-------------|
| `default` | Default content |

### Yields

| Yield | Description |
|-------|-------------|
| `Banner` | Component for rendering individual banner messages |
| `messages` | Array of current banner messages from the service |

**Usage:**
```hbs
<VBannerContainer as |container|>
  {{#each container.messages as |message|}}
    <container.Banner @message={{message}} />
  {{/each}}
</VBannerContainer>
```

---

## v-button-group

Groups buttons together with consistent styling.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `background` | "general" "dark" | "general" | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Content to render inside the button group |

---

## v-button-selector

Dropdown button that shows a menu when clicked.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `text` | string | - | no | - |
| `theme` | "neutral" "primary" "danger" "success" | "neutral" | no | - |
| `secondary` | boolean | - | no | - |
| `type` | "solid" "ghost" | "solid" | no | - |
| `iconName` | string | "Lined_Menu" | no | - |
| `iconOnly` | boolean | false | no | - |
| `size` | "regular" "small" "xsmall" | - | no | - |
| `isDisabled` | boolean | false | no | - |
| `asBlock` | boolean | false | no | - |
| `arrowSide` | "left" "right" | "right" | no | - |
| `closeOnContentClick` | boolean | false | no | - |
| `matchTriggerWidth` | boolean | true | no | Makes dropdown width equal to the trigger button width |
| `renderInPlace` | boolean | true | no | Renders dropdown inline in DOM instead of appending to `<body>` |
| `horizontalPosition` | "left" "right" "center" "auto" "auto-left" "auto-right" | "auto" | no | - |
| `verticalPosition` | "auto" "above" "below" | "below" | no | - |
| `dropdownClass` | string | - | no | - |
| `background` | "general" "dark" | "general" | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Dropdown menu content |

### Yields

| Yield | Description |
|-------|-------------|
| `close` | Action to programmatically close the dropdown |

**1. Usage with VDropdownList**

```hbs
<VButtonSelector
  @text="Actions"
  @size="xsmall"
  @horizontalPosition="right"
>
  <VDropdownList @items={{this.dropdownItems}} />
</VButtonSelector>
```
**2. Example with close action**

```hbs
<VButtonSelector @text="Actions" as |bs|>
  <button type="button" {{on "click" bs.close}}>
    Close dropdown
  </button>
</VButtonSelector>
```

---

## v-checkbox-selector

Checkbox with dropdown for bulk selection actions (select all, deselect).

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `selectedItemCount` | number | - | yes | - |
| `itemCount` | number | - | yes | - |
| `selectedItemCountOnPage` | number | - | no | - |
| `isMultiPageSelector` | boolean | false | no | - |
| `disabled` | boolean | false | no | - |
| `size` | "small" "medium" "large" | "large" | no | - |
| `verticalPosition` | "above" "below" | "below" | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `selectAllItems` | - | yes | - |
| `deselectItems` | - | yes | - |

### Blocks

| Name | Description |
|------|-------------|
| `:dropdownContent` | Custom dropdown content (replaces default select/deselect options) |

---

## v-chip

Toggleable chip/tag component for selection.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `text` | string | - | yes | - |
| `checked` | boolean | - | no | - |
| `avatar` | string | - | no | - |
| `avatarType` | "person" "corporation" | - | no | - |
| `badgeText` | string | - | no | - |
| `flag` | string | - | no | - |
| `size` | "regular" "small" | - | no | - |
| `hasActionIcon` | boolean | true | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `chipChange` | boolean | yes | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Default content |

---

## v-code-editor

Code editor component with syntax highlighting. Uses Ace editor for multi-line mode or v-textarea for one-line mode.

Dispatches a `validationStateChange` DOM event (detail: `{ errors: [] }`) when validation annotations change.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `labelText` | string | - | no | - |
| `placeholder` | string | - | no | - |
| `theme` | string | - | no | - |
| `oneline` | boolean | false | no | - |
| `mode` | "text" "css" "javascript" | "text" | no | - |
| `minLines` | number | 5 | no | - |
| `maxLines` | number | 5 | no | - |
| `readOnly` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onUpdate` | string | yes | - |
| `handleReady` | Editor | no | Called after the Ace editor instance is initialized. Use this to configure the editor directly. |
| `handleClear` | - | no | Called when the editor content is cleared via the clear button (one-line mode). |
| `handleFocus` | - | no | - |
| `handleBlur` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Optional content rendered after the editor |

---

## v-contenteditable

Contenteditable div with controlled input behavior.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `placeholder` | string | - | no | - |
| `disabled` | boolean | false | no | - |
| `autofocus` | boolean | false | no | - |
| `allowNewLines` | boolean | false | no | - |
| `allowResetValue` | boolean | false | no | - |
| `blurOnEnter` | boolean | false | no | - |
| `blurOnEscape` | boolean | false | no | - |
| `maxContentLength` | number | - | no | - |
| `clearPlaceholderOnFocus` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onChange` | string | no | - |
| `onBlur` | string, boolean | no | Called on blur. `isInternalBlurEvent` is true when blur was triggered programmatically (e.g. by `blurOnEnter` or `blurOnEscape`). |
| `onEnter` | string | no | - |
| `onEscape` | string | no | - |
| `onLengthExceeded` | number | no | Called when input is blocked because `maxContentLength` would be exceeded. Receives the attempted content length. |

---

## v-datepicker

Date picker component with calendar, time selection, and quick select menu.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `selectedDate` | null Date | null | no | - |
| `selectedTime` | { start: null \| string, end: null \| string } | { start: null, end: null } | no | - |
| `center` | null Date | null | no | - |
| `minDate` | Date | - | no | - |
| `maxDate` | Date | - | no | - |
| `withTime` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `performSave` | { selectedTime, selectedDate } | yes | Called when the user confirms the date selection. Receives the selected date and time. |
| `performCancel` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Default content |

### Yields

| Yield | Description |
|-------|-------------|
| `Calendar` | Calendar component for date/time selection |
| `Buttons` | Save/Cancel buttons component |
| `QuickMenu` | Quick select menu component |
| `actions` | Hash with `handleCalendarSelect` and `handleTimeChange` actions |

---

## v-dropdown-list

Dropdown list component for rendering a list of selectable items with optional search functionality. Commonly used inside dropdown menus.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `items` | DropdownItem[] | - | yes | - |
| `searchEnabled` | boolean | false | no | - |
| `searchPlaceholder` | string | "Search" | no | - |
| `noResultsMessage` | string | "No results found" | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onSearchInput` | string | no | - |

**Usage:**
```hbs
<VDropdownList
  @items={{this.menuItems}}
  @searchEnabled={{true}}
  @searchPlaceholder="Find action..."
  @onSearchInput={{this.handleSearch}}
/>
```
**Usage:**
```typescript
// Example items array
[
  { text: 'Edit', icon: 'Lined_Edit', action: this.handleEdit, type: 'default' },
  { text: 'Duplicate', icon: 'Lined_Copy', action: this.handleDuplicate },
  { type: 'delimiter' },
  { text: 'Delete', icon: 'Lined_Delete', action: this.handleDelete, type: 'danger' },
]
```

---

## v-editor

Rich text editor component using Trix editor.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `initialValue` | string | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `trixInitialize` | Event | no | Called when the Trix editor is ready and its element is available. |
| `trixChange` | Event | no | - |
| `trixPaste` | Event | no | - |
| `trixSelectionChange` | Event | no | - |
| `trixFocus` | Event | no | - |
| `trixBlur` | Event | no | - |
| `trixFileAccept` | Event | no | Called when a file is being attached. Call `event.preventDefault()` to reject the file. |
| `trixAttachmentAdd` | Event | no | Called when an attachment (image, file) is added to the editor content. |
| `trixAttachmentRemove` | Event | no | Called when an attachment is removed from the editor content. |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Optional content rendered after the editor |

---

## v-empty

Empty state component for displaying placeholder content.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `isCentered` | boolean | false | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `:icon` | Icon to display at the top |
| `:title` | Title text (required) |
| `:description` | Description text below the title |
| `:button` | Action button at the bottom |

---

## v-helper

Helper icon with tooltip for contextual information.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `type` | "info" "attention" "warning" | "info" | no | - |
| `fill` | "solid" "lined" | "lined" | no | - |
| `background` | "general" "dark" | "general" | no | - |
| `side` | "left" "right" "top" "bottom" | "right" | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Tooltip content |

---

## v-input-date

Date input with calendar dropdown for selecting single or range dates.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `startDate` | null string number Date | - | no | - |
| `endDate` | null string number Date | - | no | - |
| `ranged` | boolean | false | no | - |
| `error` | boolean | false | no | - |
| `startDateWithError` | boolean | false | no | - |
| `endDateWithError` | boolean | false | no | - |
| `startDatePlaceholder` | null string | - | no | - |
| `endDatePlaceholder` | null string | - | no | - |
| `showTime` | boolean | false | no | - |
| `showTimezone` | boolean | false | no | - |
| `showQuickMenu` | boolean | false | no | - |
| `renderInPlace` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `handlePicker` | SelectedDateResult | yes | Called when the user confirms the date selection in the calendar dropdown. |
| `handleCancel` | - | no | - |
| `handleClear` | "startDate" \| "endDate" | no | Called when the user clears a date field. Receives which field was cleared. |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Optional content rendered after the input |

---

## v-input-invisible

Minimal inline text input using contenteditable.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `placeholder` | string | - | no | - |
| `disabled` | boolean | false | no | - |
| `theme` | "default" "error" | "default" | no | - |
| `size` | "small" "regular" "big" | "regular" | no | - |
| `maxWidth` | number | - | no | - |
| `maxContentLength` | number | - | no | - |
| `errorText` | string | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onChange` | string | no | - |
| `onSave` | string | no | Called on Enter key press or when the field loses focus. |
| `onCancel` | string | no | Called on Escape key press. The value is reverted to the original before calling. |

---

## v-input-password

Password input with show/hide toggle and validation.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `placeholder` | string | - | no | - |
| `labelText` | string | - | no | - |
| `labelPosition` | "inside" "outside" | "outside" | no | - |
| `hintText` | string | - | no | - |
| `isDisabled` | boolean | false | no | - |
| `canBeValidated` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onInput` | string | no | - |
| `onBlur` | - | no | - |
| `onSubmit` | - | no | - |

---

## v-input-submit

Text input with submit button for search-like functionality.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `placeholder` | string | - | no | - |
| `isDisabled` | boolean | false | no | - |
| `form` | "squared" "rounded" "no-border-radius" | "squared" | no | - |
| `size` | string | - | no | - |
| `minLength` | number | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onInput` | string | no | - |
| `onSubmit` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `:button` | Custom submit button (replaces default search icon button) |

---

## v-input-text

Text input component with label, icon, hints, and clear button.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `value` | string | - | yes | - |
| `placeholder` | string | "" | no | - |
| `type` | string | "text" | no | - |
| `theme` | "default" "error" "success" "light" | "default" | no | - |
| `form` | "squared" "rounded" "no-border-radius" | "squared" | no | - |
| `size` | "regular" "small" "xsmall" | - | no | - |
| `labelText` | string | - | no | - |
| `labelPosition` | "inside" "outside" | "outside" | no | - |
| `iconName` | string | - | no | - |
| `hintText` | string | - | no | - |
| `maxLength` | string number | - | no | - |
| `pattern` | string | - | no | Regexp pattern to validate input on keypress and paste |
| `isDisabled` | boolean | false | no | - |
| `isEmbeded` | boolean | false | no | - |
| `hasClearButton` | boolean | true | no | - |
| `bordered` | boolean | true | no | - |
| `borderPosition` | "outside" "inside" "both" | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onInput` | string | yes | - |
| `onFocus` | - | no | - |
| `onBlur` | string | no | - |
| `onSubmit` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Content rendered in controls area (after clear button) |
| `:leftContent` | Content rendered before the input field |

---

## v-loader

Loading state component with spinner and optional text.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `title` | string | - | no | - |
| `description` | string | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Optional content rendered after the loader |

---

## v-message

Notification/alert message component with different types and optional actions.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `type` | "success" "info" "warning" "error" | "info" | no | - |
| `text` | string | - | no | - |
| `header` | string | - | no | - |
| `badgeText` | string | - | no | - |
| `hasIcon` | boolean | false | no | - |
| `hasCloseButton` | boolean | false | no | - |
| `hasActionButton` | boolean | false | no | - |
| `actionButtonText` | string | - | no | - |
| `actionButtonIcon` | string | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `closeAction` | - | no | Called when the close button is clicked. Requires `hasCloseButton` to be true. |
| `buttonAction` | - | no | Called when the action button is clicked. Requires `hasActionButton` to be true. |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Message content (replaces `text` argument) |
| `:icon` | Custom icon (replaces default type-based icon) |
| `:rightContent` | Custom content on the right side |

---

## v-modal

Modal dialog component with header, content, and footer.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `isVisible` | boolean | - | yes | - |
| `title` | string | - | no | - |
| `subtitle` | string | - | no | - |
| `prompt` | boolean | false | no | - |
| `noAnimation` | boolean | false | no | - |
| `noHeader` | boolean | false | no | - |
| `noFooter` | boolean | false | no | - |
| `hideCloseButton` | boolean | false | no | - |
| `hideCancelButton` | boolean | false | no | - |
| `hideConfirmButton` | boolean | false | no | - |
| `cancelText` | string | "Cancel" | no | - |
| `confirmText` | string | "OK" | no | - |
| `confirmDisabled` | boolean | false | no | - |
| `confirmLoading` | boolean | false | no | - |
| `confirmTheme` | string | "primary" | no | - |
| `height` | string | - | no | - |
| `targetSelector` | string | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onCancel` | - | yes | - |
| `onClose` | - | no | Called when the modal is dismissed (overlay click, Escape key, close button). Falls back to `onCancel` if not provided. Optional, prefer to use onCancel instead. |
| `onConfirm` | - | no | - |
| `onInsert` | HTMLElement | no | Called when the modal wrapper element is inserted into the DOM. |
| `onDestroy` | - | no | Called when the modal is removed from the DOM. |
| `animateShow` | - | no | Hook called after the show animation starts. Use for custom animation logic. |
| `animateHide` | - | no | Hook called after the hide animation starts. Use for custom animation logic. |

### Blocks

| Name | Description |
|------|-------------|
| `:title` | Custom title content |
| `:headerSlot` | Additional header content below title |
| `:content` | Main modal content |
| `:footer` | Custom footer (replaces default buttons) |
| `:greeting` | Greeting content outside modal |

**1. Basic example**
For most use cases, only `onCancel` is needed. Use `onClose` only when you need to distinguish between the user clicking the Cancel button vs dismissing the modal via close button, overlay, or Escape key.

```hbs
<VModal
  @isVisible={{this.showModal}}
  @title="Confirm action"
  @cancelText="Cancel"
  @confirmText="Save"
  @onCancel={{this.close}}
  @onConfirm={{this.save}}
>
  <:content>
    Modal body content here.
  </:content>
</VModal>
```
**2. Footer buttons: Prefer built-in props over custom `<:footer>`**
For standard 2-button modals, always use the built-in footer props:

```hbs
{{!-- ✅ Preferred --}}
<VModal
  @cancelText="Cancel"
  @confirmText="Save"
  @onCancel={{this.close}}
  @onConfirm={{this.save}}
/>

{{!-- ❌ Avoid when not needed --}}
<VModal>
  <:footer>
    <v-button text="Cancel" ... />
    <v-button text="Save" ... />
  </:footer>
</VModal>
```

Only use <:footer> when:
- You need more than 2 buttons
- You need non-standard button sizes (built-in uses "small")
- You need different layout (e.g., buttons on left side)

---

## v-pagination

Pagination controls for navigating through pages.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `content` | { page: number, totalPages: number } | - | yes | - |
| `pagesToShow` | number | 3 | no | - |
| `showFL` | boolean | false | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onClick` | number | no | - |

---

## v-pagination-per-page

Per-page selector for pagination.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `active` | number | - | yes | - |
| `values` | number[] | - | no | - |
| `label` | string | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onClick` | number | yes | - |

---

## v-player

Video player overlay with support for multiple videos (YouTube, Wistia).

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `isShown` | boolean | - | yes | - |
| `videos` | null Video[] | - | yes | - |
| `currentVideo` | null Video | - | yes | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onClose` | - | no | - |
| `setCurrentVideo` | Video | no | Called when the user navigates to a different video via the previous/next buttons. |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Additional content in the player |
| `:dialog` | Dialog content overlay |
| `:footer` | Footer content below the video |

---

## v-select

Dropdown select component built on ember-power-select.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `options` | unknown[] | - | yes | - |
| `selected` | unknown | - | no | - |
| `multiple` | boolean | false | no | - |
| `closeOnSelect` | boolean | - | no | - |
| `allowClear` | boolean | - | no | - |
| `placeholder` | string | - | no | - |
| `hintText` | string | - | no | - |
| `labelText` | string | - | no | - |
| `labelPosition` | "inside" "outside" | "outside" | no | - |
| `optionKey` | string | - | no | - |
| `size` | "xsmall" "xsmall-compact" "small" "regular" | "regular" | no | - |
| `theme` | "error" "default" "light" | "default" | no | - |
| `disabled` | boolean | false | no | - |
| `inline` | boolean | false | no | - |
| `iconOnly` | boolean | false | no | - |
| `iconName` | string | - | no | - |
| `triggerClass` | string | - | no | - |
| `dropdownClass` | string | - | no | - |
| `matchTriggerWidth` | boolean | - | no | - |
| `allowTextWrap` | boolean | true | no | - |
| `searchEnabled` | boolean | false | no | - |
| `searchField` | string | - | no | - |
| `searchPlaceholder` | string | - | no | - |
| `renderInPlace` | boolean | - | no | - |
| `verticalPosition` | "auto" "above" "below" | - | no | - |
| `horizontalPosition` | "left" "right" "center" "auto" "auto-left" "auto-right" | - | no | - |
| `triggerComponent` | string object | - | no | - |
| `selectedItemComponent` | string object | - | no | - |
| `optionsComponent` | string object | - | no | - |
| `beforeOptionsComponent` | string object | - | no | - |
| `extra` | Record<string, unknown> | - | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onChange` | selected item | yes | Called when the selection changes. The second argument is the ember-power-select API object. |
| `search` | searchTerm: string | no | Custom search function that overrides default filtering. Can return a Promise for async search. |
| `onOpen` | unknown | no | - |
| `onOptionMouseUp` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Custom option rendering. Receives `option` as block param |

---

## v-submit-button

Button that triggers form submission.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `asBlock` | boolean | false | no | - |

---

## v-tooltip

Tooltip/popover component.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `text` | string | - | no | - |
| `side` | "left" "right" "top" "bottom" | "top" | no | - |
| `delay` | number | 200 | no | - |
| `event` | "hover" "click" "focus" "none" | "hover" | no | - |
| `isShown` | boolean | - | no | - |
| `isAdvanced` | boolean | false | no | - |
| `oneLineText` | boolean | false | no | - |
| `withCloseButton` | boolean | false | no | - |
| `popperContainer` | string false | document.body | no | - |
| `popoverHideDelay` | number | 100 | no | - |

### Actions

| Action | Payload | Required | Description |
|--------|---------|----------|-------------|
| `onTooltipClose` | - | no | - |

### Blocks

| Name | Description |
|------|-------------|
| `default` | Custom tooltip content (replaces `text` argument) |

---

## v-tooltip-overflow

Renders text with ellipsis truncation and shows a VTooltip only when the text overflows its container.

The component renders a `<span>` with overflow styles and a sibling `<VTooltip>`.
Place inside a flex or grid container so the span can shrink and trigger overflow.
Do not place other elements inside of the parent wrapper.

### Arguments

| Argument | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `text` | string | - | yes | - |
| `side` | "left" "right" "top" "bottom" | "top" | no | - |
| `delay` | number | 200 | no | - |
| `observe` | boolean | true | no | Enable ResizeObserver to recheck overflow on resize. |

**Usage:**
```hbs
<div style="display: flex; width: 200px;">
  <VTooltipOverflow @text="Long text that will be truncated" @side="left" />
</div>
```

