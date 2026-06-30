import { useEffect, useRef, useImperativeHandle, forwardRef } from "react";

const SITE_KEY = import.meta.env.VITE_TURNSTILE_SITE_KEY;

const Turnstile = forwardRef(function Turnstile({ onVerify, action }, ref) {
  const containerRef = useRef(null);
  const widgetId = useRef(null);

  useEffect(() => {
    if (!SITE_KEY) {
      onVerify("local-development-token");
      return;
    }

    let interval;
    const tryRender = () => {
      if (window.turnstile && containerRef.current && widgetId.current === null) {
        widgetId.current = window.turnstile.render(containerRef.current, {
          sitekey: SITE_KEY,
          action,
          callback: onVerify,
          "expired-callback": () => onVerify(""),
          "error-callback": () => onVerify(""),
        });
        clearInterval(interval);
      }
    };
    interval = setInterval(tryRender, 100);
    tryRender();

    return () => {
      clearInterval(interval);
      if (window.turnstile && widgetId.current !== null) {
        window.turnstile.remove(widgetId.current);
        widgetId.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useImperativeHandle(ref, () => ({
    reset: () => {
      if (window.turnstile && widgetId.current !== null) {
        window.turnstile.reset(widgetId.current);
      }
    },
  }));

  if (!SITE_KEY) {
    return (
      <div className="turnstile-fallback">
        Verification is disabled for local development.
      </div>
    );
  }

  return <div ref={containerRef} />;
});

export default Turnstile;
