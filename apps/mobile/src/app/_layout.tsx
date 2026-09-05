import React, { useEffect, useState } from "react";
import { Animated, Image, StyleSheet, Text, View } from "react-native";
import * as SplashScreen from "expo-splash-screen";
import { Stack } from "expo-router";

void SplashScreen.preventAutoHideAsync();

function HeritageAISplash({
  onComplete,
}: {
  onComplete: () => void;
}) {
  const [opacity] = useState(() => new Animated.Value(0));
  const [scale] = useState(() => new Animated.Value(0.82));
  const [taglineOpacity] = useState(() => new Animated.Value(0));
  const [exitOpacity] = useState(() => new Animated.Value(1));

  useEffect(() => {
    const animation = Animated.sequence([
      Animated.parallel([
        Animated.timing(opacity, {
          toValue: 1,
          duration: 700,
          useNativeDriver: true,
        }),
        Animated.spring(scale, {
          toValue: 1,
          friction: 7,
          tension: 45,
          useNativeDriver: true,
        }),
      ]),
      Animated.timing(taglineOpacity, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.delay(900),
      Animated.timing(exitOpacity, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }),
    ]);

    animation.start(({ finished }) => {
      if (finished) {
        onComplete();
      }
    });

    return () => animation.stop();
  }, [exitOpacity, opacity, scale, taglineOpacity, onComplete]);

  return (
    <Animated.View
      style={[
        styles.splash,
        {
          opacity: exitOpacity,
        },
      ]}
    >
      <Animated.View
        style={{
          alignItems: "center",
          opacity,
          transform: [{ scale }],
        }}
      >
        <Image
          source={require("../../assets/icon.png")}
          style={styles.logo}
          resizeMode="contain"
        />

        <Text style={styles.brand}>HERITAGEAI</Text>

        <View style={styles.divider} />

        <Animated.Text
          style={[
            styles.tagline,
            {
              opacity: taglineOpacity,
            },
          ]}
        >
          Discover. Understand. Preserve.
        </Animated.Text>
      </Animated.View>
    </Animated.View>
  );
}

export default function RootLayout() {
  const [showSplash, setShowSplash] = useState(true);

  const completeSplash = React.useCallback(async () => {
    setShowSplash(false);
    await SplashScreen.hideAsync();
  }, []);

  return (
    <>
      <Stack
        screenOptions={{
          headerShown: false,
        }}
      />

      {showSplash && <HeritageAISplash onComplete={completeSplash} />}
    </>
  );
}

const styles = StyleSheet.create({
  splash: {
    ...StyleSheet.absoluteFill,
    zIndex: 9999,
    backgroundColor: "#0B0907",
    alignItems: "center",
    justifyContent: "center",
  },
  logo: {
    width: 150,
    height: 150,
  },
  brand: {
    marginTop: 10,
    fontSize: 18,
    fontWeight: "700",
    letterSpacing: 4,
    color: "#E7B94A",
  },
  divider: {
    width: 52,
    height: 1,
    marginTop: 16,
    marginBottom: 14,
    backgroundColor: "#E7B94A",
  },
  tagline: {
    fontSize: 12,
    letterSpacing: 1.4,
    color: "#C7BDAA",
  },
});


