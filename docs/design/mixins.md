# SCSS Mixins

Available SCSS mixins in `universe-variables` package. Use these instead of writing raw CSS for consistency.

## Typography

### `font-family($fontname: 'Geist')`
Sets font family with variable font support. Default uses Geist with OpenType features enabled.

```scss
@include font-family();           // Uses Geist with feature settings
@include font-family('Arial');    // Uses custom font
```

### `font-regular($size: h4)`
Applies regular weight (500) typography with predefined sizes.

| Size | Font Size | Line Height | Letter Spacing |
|------|-----------|-------------|----------------|
| h2   | 22px      | 32px        | -0.01em        |
| h3   | 18px      | 24px        | -              |
| h4   | 14px      | 24px        | -              |
| h5   | 12px      | 16px        | 0.01em         |

```scss
@include font-regular(h3);
```

### `font-bold($size: h4)`
Applies bold weight (550) typography with same size variants as `font-regular`.

```scss
@include font-bold(h2);
```

### `big-numbers()`
Large number display style (32px, weight 450).

```scss
@include big-numbers();
```

## Accessibility

### `visually-hidden()`
Hides content visually while keeping it accessible to screen readers.

```scss
@include visually-hidden();
```

### `focus-visible-outline()`
Standard focus outline for keyboard navigation (2px solid black, 2px offset).

```scss
&:focus-visible {
  @include focus-visible-outline();
}
```

## Animation

### `transition-property($properties...)`
Creates smooth transitions for properties using design system timing values.

```scss
@include transition-property(opacity, transform);
// Generates: transition: opacity 150ms ease, transform 150ms ease;
```

## Box Shadow

### `box-shadow($color, $width)`
Inner (inset) box shadow, useful for borders that don't affect layout.

```scss
@include box-shadow(var(--color-border), 1px);
// Generates: box-shadow: inset 0 0 0 1px var(--color-border);
```

### `outer-box-shadow($color, $width)`
Outer box shadow, useful for focus rings or elevation effects.

```scss
@include outer-box-shadow(var(--color-focus), 2px);
// Generates: box-shadow: 0 0 0 2px var(--color-focus);
```

## Scrollbar

### `scrollbar-default()`
Standard scrollbar styling (auto width). Cross-browser compatible.

```scss
.scrollable-container {
  @include scrollbar-default();
}
```

### `scrollbar-thin()`
Thin scrollbar styling. Cross-browser compatible.

```scss
.compact-list {
  @include scrollbar-thin();
}
```
